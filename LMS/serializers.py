from django.contrib.auth.models import User , Group
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.exceptions import *
from .models import *
import random, string



class QPartSerializer(serializers.ModelSerializer):
    class Meta:
        model = QPart
        fields = ('pk' , 'mode' , 'txt', 'image' )



class SubjectSerializer(serializers.ModelSerializer):
    topic_count = serializers.SerializerMethodField()
    class Meta:
        model = Subject
        fields = ('pk' , 'created' , 'title', 'level' , 'description' , 'dp' , 'topic_count')

    def get_topic_count(self, obj):
        return obj.topics.all().count()

class TopicSerializer(serializers.ModelSerializer):
    subject = SubjectSerializer(many = False , read_only = True)
    class Meta:
        model = Topic
        fields = ('pk' , 'created' , 'subject', 'title' , 'description' )

    def create(self , validated_data):
        print 'came here'
        print self.context['request'].data['subject']
        t = Topic(**validated_data)
        t.subject = Subject.objects.get(pk = self.context['request'].data['subject'])
        t.save()
        return t



class SubjectLiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ('pk'  , 'title', 'level' )

class TopicLiteSerializer(serializers.ModelSerializer):
    subject = SubjectLiteSerializer(many = False , read_only = True)
    class Meta:
        model = Topic
        fields = ('pk', 'title' , 'subject' )


class QuestionSerializer(serializers.ModelSerializer):
    quesParts = QPartSerializer(many = True , read_only = True)
    optionsParts = QPartSerializer(many = True , read_only = True)
    topic = TopicLiteSerializer(many = False , read_only = True)

    class Meta:
        model = Question
        fields = ('pk' , 'created' , 'updated', 'ques' , 'quesParts' , 'optionsParts' , 'solutionParts' , 'status', 'archived' , 'topic', 'level' , 'marks' , 'qtype' , 'codeLang' , 'user')
        read_only_fields = ('archived', 'approved', 'reviewed', 'forReview' , 'user')

    def create(self , validated_data):
        q = Question(**validated_data)
        q.user = self.context['request'].user
        q.save()
        return q

    def update(self , instance , validated_data):
        if 'qPartToAdd' in self.context['request'].data:
            instance.quesParts.add(QPart.objects.get(pk = self.context['request'].data['qPartToAdd'] ))

        if 'qOptionToAdd' in self.context['request'].data:
            instance.optionsParts.add(QPart.objects.get(pk = self.context['request'].data['qOptionToAdd'] ))

        if 'ques' in validated_data:
            instance.ques = validated_data.pop('ques')
            instance.topic_id = self.context['request'].data['topic']
            instance.level = validated_data.pop('level')
            instance.qtype = validated_data.pop('qtype')


        if instance.qtype not in ['mcq' , 'mcc']:
            instance.optionsParts.clear()

        instance.save()

        return instance

class PaperSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many = True , read_only = True)
    class Meta:
        model = Paper
        fields = ('pk' , 'created' , 'updated', 'level', 'questions', 'active' , 'topic' , 'user')
        read_only_fields = ('user', )


class AnswerSerializer(serializers.ModelSerializer):
    subject = SubjectSerializer(many = False , read_only = True)
    class Meta:
        model = Answer
        fields = ('pk' , 'created' , 'question', 'paper' , 'evaluated' , 'correct', 'marksObtained' , 'attachment', 'txt' , 'subject')
        read_only_fields = ('user', )

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('pk' , 'created' , 'txt', 'user')

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ('pk' , 'created' , 'user' )

class StudyMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyMaterial
        fields = ('pk' , 'created' , 'typ', 'attachment', 'archived', 'course' , 'pinned' , 'likes'  , 'comments' , 'user', )
        read_only_fields = ('user', 'likes' , 'comments')
    def create(self , validated_data):
        sm = StudyMaterial(**validated_data)
        sm.user = self.context['request'].user
        sm.save()
        return sm

class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = ('pk' , 'created' , 'course', 'addedBy', 'accepted', 'user' , 'active' )
        read_only_fields = ('addedBy',)
    def create(self , validated_data):
        e = Enrollment(**validated_data)
        e.addedBy = self.context['request'].user
        e.accepted = True
        e.save()
        return e

class CourseSerializer(serializers.ModelSerializer):
    enrollments = EnrollmentSerializer(many = True , read_only = True)
    studyMaterials = StudyMaterialSerializer(many = True , read_only = True)
    class Meta:
        model = Course
        fields = ('pk' , 'created' , 'updated', 'topic', 'enrollmentStatus', 'instructor' , 'TAs' , 'user' , 'description' , 'title' , 'enrollments' , 'studyMaterials')
        read_only_fields = ('user', 'TAs')
    def create(self , validated_data):
        c = Course(**validated_data)
        c.user = self.context['request'].user
        c.save()

        for u in self.context['request'].data['TAs']:
            c.TAs.add(User.objects.get(pk = u))
        return c
