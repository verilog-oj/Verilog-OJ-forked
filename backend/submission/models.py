from django.db import models

from problem.models import Problem, TestCase
from file.models import File
from user.models import User

class Submission(models.Model):
    id = models.AutoField(primary_key=True, help_text='提交ID')
    problem = models.ForeignKey(
        Problem,
        on_delete=models.SET_NULL, null=True,
        help_text='提交的题目',
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        help_text='提交的用户'
    )
    submit_time = models.DateTimeField(auto_now_add=True, help_text='提交时间')
    submit_files = models.ManyToManyField(File, help_text='提交的文件（代码等）')
    
    def get_results(self):
        return SubmissionResult.objects.filter(submission=self)
    def get_total_grade(self):
        return sum([result.grade for result in self.get_results()])
    def have_judged(self):
        return self.get_results().exists()

class SubmissionResult(models.Model):
    id = models.AutoField(primary_key=True, help_text='提交结果ID')
    submit_time = models.DateTimeField(auto_now_add=True, help_text='结果提交时间')
    submission = models.ForeignKey(
        Submission,
        on_delete=models.CASCADE,
        help_text='某个测试点结果所属的提交'
    )
    testcase = models.ForeignKey(
        TestCase,
        on_delete=models.CASCADE,
        help_text='某个测试点结果所属的测试点'
    )
    grade = models.IntegerField(help_text='本测试点所得的分数')
    log = models.TextField(help_text='The log generated along the process')
    app_data = models.TextField(help_text='Data associated with this result (waveform, etc)')
    
    class Meta:
        unique_together = (('submission', 'testcase'),)