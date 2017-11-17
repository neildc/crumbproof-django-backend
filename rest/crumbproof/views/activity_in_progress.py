from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import generics
from rest_framework.decorators import detail_route
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.utils.timezone import now

from crumbproof.models import ActivityInProgress, ScheduledPushNotification
from crumbproof.serializers import ActivityInProgressSerializer
from crumbproof.permissions import IsOwner

import datetime
from datetime import timedelta


class LiveActivityStart(generics.CreateAPIView):
    serializer_class = ActivityInProgressSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class LiveActivity(generics.RetrieveDestroyAPIView):
    serializer_class = ActivityInProgressSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwner)

    def get_object(self):
        return get_object_or_404(ActivityInProgress, user=self.request.user)

    def perform_destroy(self, instance):
        instance.delete()

def getInstruction(activity, step_number):
    return activity.recipe.data['instructions'][step_number]


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def liveActivityNextStep(request):

    # TODO: Delete all push stray push notifications
    activity = get_object_or_404(ActivityInProgress, user=request.user)
    curr_step = activity.current_step

    # instruction = getInstruction(activity, curr_step)

    time_now = str(now())

    #TODO: see if we need to handle this

    # # Start time is normally inserted by the timer start endpoint
    # if time_gap_to_next not in instruction:
    #    activity.start_times[instruction['id']] = time_now

    # prev_instruction_id = getInstruction(activity, curr_step - 1)['id']
    # if curr_step > 1 \
    #    and not prevInstruction['id'] in activity.start_times:
    #    activity.start_times[prev_instruction_id] = time_now

    prev_instruction_id = getInstruction(activity, curr_step)['id']
    activity.end_times[prev_instruction_id] = time_now

    activity.current_step = curr_step + 1;

    activity.save()

    return Response(
        {
            "end_times": {prev_instruction_id : time_now},
            "current_step" : curr_step + 1
        }
    )

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def liveActivityStartTimer(request):
    activity = get_object_or_404(ActivityInProgress, user=request.user)
    curr_step = activity.current_step
    time_now = now()

    instruction = getInstruction(activity, curr_step)
    instruction_id = instruction['id']
    activity.start_times[instruction_id] = str(time_now)
    activity.save()

    if 'time_gap_to_next' in instruction:
        # Round down to the minute
        launch_time = time_now.replace(microsecond=0,second=0) \
                      + timedelta(minutes=instruction['time_gap_to_next'])

        push = ScheduledPushNotification(launch_time=launch_time,
                                         user=request.user,
                                         data="Time is done")

        push.save()


    return Response(
        {
            "start_times": {instruction_id : time_now},
        }
    )
