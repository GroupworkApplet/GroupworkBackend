from rest_framework import views
from rest_framework.response import Response
from rest_framework import status

from .serializers import *
from .models import *

import logging


# 所有组的接口
class GroupList(views.APIView):

    def get(self, request):
        try:
            groups = Group.objects.all()
        except Group.DoesNotExist():
            return Response({'message': '查询对象不存在'},
                            status=status.HTTP_404_NOT_FOUND)
        group_list = GroupSerializer(instance=groups, many=True)
        return Response(group_list.data, status=status.HTTP_200_OK)

    def post(self, request):
        group_set = GroupSerializer(data=request.data, many=True)
        if group_set.is_valid():
            group_set.save()
            return Response(group_set.data, status=status.HTTP_200_OK)
        else:
            return Response({'message': '传入数据错误'},
                            status=status.HTTP_400_BAD_REQUEST)


# 某个组的接口
class GroupDetail(views.APIView):

    @staticmethod
    # 判断查找的group是否存在
    def find_group(pk):
        try:
            group = Group.objects.get(pk=pk)
            return group
        except Group.DoesNotExist:
            return False

    def get(self, request, pk):
        group = self.find_group(pk)
        if not group:
            return Response({'message': '请求的组群不存在'},
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            group_serializer = GroupSerializer(instance=group)
            return Response(group_serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        group = self.find_group(pk)
        if not group:
            return Response({'message': '要更新的组群不存在'},
                            status=status.HTTP_400_BAD_REQUEST)
        new_group = GroupSerializer(instance=group, data=request.data)
        if new_group.is_valid():
            new_group.save()
            return Response(new_group.data, status=status.HTTP_200_OK)
        else:
            return Response({'message': '传入数据错误'},
                            status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        group = self.find_group(pk)
        if not group:
            return Response({'message': '要删除的组群不存在'},
                            status=status.HTTP_400_BAD_REQUEST)
        group.delete()
        return Response({'message': '删除小组成功'},
                        status=status.HTTP_204_NO_CONTENT)


# 某个组的所有组员的接口
class GroupMemberList(views.APIView):

    def get(self, request, group_id):
        try:
            members = GroupMember.objects.filter(group_id=group_id)
        except GroupMember.DoesNotExist():
            return Response({'message': '查询对象不存在'}, status=status.HTTP_404_NOT_FOUND)

        return Response(
            GroupMemberSerializer(members, many=True).data,
            status=status.HTTP_200_OK)

    def post(self, request, group_id):
        member_set = GroupMemberSerializer(data=request.data, many=True)
        if not member_set.is_valid():
            return Response({'message': '传入数据错误'}, status=status.HTTP_400_BAD_REQUEST)
        member_set.save()
        return Response(member_set.data, status=status.HTTP_200_OK)


# 一个组的某个组员的接口
class GroupMemberDetail(views.APIView):
    @staticmethod
    def find_group_member(pk):
        try:
            member = GroupMember.objects.get(pk=pk)
            return member
        except GroupMember.DoesNotExist:
            return False

    def get(self, request, pk, group_id):
        member = self.find_group_member(pk)
        if not member:
            return Response({'message': '请求的组员不存在'},
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                GroupMemberSerializer(instance=member).data,
                status=status.HTTP_200_OK)

    def put(self, request, pk, group_id):
        member = self.find_group_member(pk)
        if not member:
            return Response({'message': '要更新的组员不存在'},
                            status=status.HTTP_400_BAD_REQUEST)
        new_member = GroupMemberSerializer(instance=member, data=request.data)
        if new_member.is_valid():
            new_member.save()
            return Response(new_member.data, status=status.HTTP_200_OK)
        else:
            return Response({'message': '传入数据错误'},
                            status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, group_id):
        member = self.find_group_member(pk)
        if not member:
            return Response({'message': '要删除的组员不存在'},
                            status=status.HTTP_400_BAD_REQUEST)
        member.delete()
        return Response({'message': '删除组员成功成功'},
                        status=status.HTTP_204_NO_CONTENT)


# 一个group中所有消息的接口
class MessageList(views.APIView):

    def get(self, request, group_id):
        try:
            messages = Message.objects.filter(group_id=group_id)
        except Message.DoesNotExist:
            return Response({'message': '查询对象不存在'}, status=status.HTTP_404_NOT_FOUND)

        return Response(
            MessageSerializer(messages, many=True).data,
            status=status.HTTP_200_OK)

    def post(self, request, group_id):
        message_set = MessageSerializer(data=request.data, many=True)
        if not message_set.is_valid():
            return Response({'message': '传入数据错误'}, status=status.HTTP_400_BAD_REQUEST)
        '''
        if message_set.data['group'] != group_id:
            return Response({'message': '传入数据矛盾'}, status=status.HTTP_400_BAD_REQUEST)
        '''
        return Response(message_set.data, status=status.HTTP_200_OK)


# 某条消息的接口
class MessageDetail(views.APIView):
    @staticmethod
    def find_message(pk):
        try:
            message = Message.objects.get(pk=pk)
            return message
        except Message.DoesNotExist():
            return False

    def get(self, request, pk, group_id):
        message = self.find_message(pk)
        if not message:
            return Response({'message': '请求的消息不存在'},
                            status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(
                MessageSerializer(instance=message).data,
                status=status.HTTP_200_OK)

    def delete(self, request, pk, group_id):
        message = self.find_message(pk)
        if not message:
            return Response({'message': '要删除的消息不存在'},
                            status=status.HTTP_404_NOT_FOUND)
        message.delete()
        return Response({'message': '删除消息成功成功'},
                        status=status.HTTP_204_NO_CONTENT)


# 一个group里面所有文档的接口
class DocumentList(views.APIView):

    @staticmethod
    def get_group(group_id):
        try:
            group = Group.objects.get(pk=group_id)
        except Group.DoesNotExist:
            return False
        return group

    def get(self, request, group_id):

        group = self.get_group(group_id)
        if not group:
            return Response({'message': '对应组群不存在'}, status=status.HTTP_404_NOT_FOUND)
        try:
            documents = Document.objects.filter(group_id=group_id)
        except Document.DoesNotExist():
            return Response({'message': '查询对象不存在'}, status=status.HTTP_404_NOT_FOUND)

        return Response(
            DocumentSerializer(documents, many=True).data,
            status=status.HTTP_200_OK)

    def post(self, request, group_id):
        document_set = DocumentSerializer(data=request.data)
        if document_set.is_valid():
            document_set.save()
            return Response(document_set.data, status=status.HTTP_200_OK)
        else:
            return Response({'message': '传入数据错误'}, status=status.HTTP_400_BAD_REQUEST)


# 对一个group中某个文档的查询
class DocumentDetail(views.APIView):
    @staticmethod
    def find_document(pk):
        try:
            document = Document.objects.get(pk=pk)
            return document
        except Document.DoesNotExist():
            return False

    def get(self, request, pk, group_id):
        document = self.find_document(pk)
        if not document:
            return Response({'message': '请求的文档不存在'},
                            status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(
                DocumentSerializer(instance=document).data,
                status=status.HTTP_200_OK)

    def delete(self, request, pk, group_id):
        document = self.find_document(pk)
        if not document:
            return Response({'message': '要删除的文档不存在'},
                            status=status.HTTP_404_NOT_FOUND)
        document.delete()
        return Response({'message': '删除文档成功成功'},
                        status=status.HTTP_204_NO_CONTENT)


# 一个group中的progress的接口
class ProgressDetail(views.APIView):
    @staticmethod
    def find_progress(group_id):
        try:
            group = Group.objects.get(pk=group_id)
            progress = Progress.objects.get(group=group)
        except Group.DoesNotExist:
            return False
        except Progress.DoesNotExist:
            return False
        return progress

    def get(self, request, group_id):
        progress = self.find_progress(group_id)
        if not progress:
            return Response({'message': '请求数据不存在'},
                            status=status.HTTP_404_NOT_FOUND)
        return Response(
            ProgressSerializer(instance=progress).data,
            status=status.HTTP_200_OK
        )

    def post(self, request, group_id):
        try:
            group = Group.objects.get(pk=group_id)
        except Group.DoesNotExist:
            return Response({'message': '请求的小组不存在'},
                            status=status.HTTP_404_NOT_FOUND)
        progress = ProgressSerializer(data=request.data)
        if not progress.is_valid():
            return Response({'message': '传入数据不合法'},
                            status=status.HTTP_400_BAD_REQUEST)
        if progress.validated_data.get('group').id != group_id:
            return Response({'message': '传入数据不匹配'},
                            status=status.HTTP_400_BAD_REQUEST)
        progress.save()
        return Response(progress.data, status=status.HTTP_200_OK)

    def put(self, request, group_id):
        progress = self.find_progress(group_id)
        if not progress:
            return Response({'message': '请求数据不存在'},
                            status=status.HTTP_404_NOT_FOUND)
        new_progress = ProgressSerializer(instance=progress, data=request.data)
        if not new_progress.is_valid():
            return Response({'message': '传入数据不合法'},
                            status=status.HTTP_400_BAD_REQUEST)
        if new_progress.validated_data.get('group').id != group_id:
            return Response({'message': '数据不匹配'},
                            status=status.HTTP_400_BAD_REQUEST)
        new_progress.save()
        return Response(new_progress.data, status=status.HTTP_200_OK)
