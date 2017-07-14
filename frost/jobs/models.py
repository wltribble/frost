import datetime

from django.db import models

# Create your models here.
class Job(models.Model):
    jmojobid = models.CharField(db_column='jmoJobID', max_length=20)
    jmojobassemblyid = models.IntegerField(db_column='jmoJobAssemblyID')
    jmojoboperationid = models.IntegerField(db_column='jmoJobOperationID')
    jmoprocesslongdescriptiontext = models.TextField(
                                    db_column='jmoProcessLongDescriptionText'
                                    )
    jmoworkcenterid = models.CharField(
                                db_column='jmoworkcenterid',
                                max_length=5
                                )
    jmocreateddate = models.DateTimeField(db_column='jmoCreatedDate',
                                blank=True, null=True
                                )
    jmouniqueid = models.CharField(db_column='jmoUniqueID',
                                unique=True, max_length=36,
                                editable=False, primary_key=True
                                )

    class Meta:
        managed = False
        db_table = 'JobOperations'
        unique_together = (('jmojobid',
                            'jmojobassemblyid', 'jmojoboperationid'),
                            )

    def __str__(self):
        return (str(self.jmojobid) + " -- " + str(self.jmojobassemblyid)
                + " -- " + str(self.jmojoboperationid)
                )


class FieldManager(models.Manager):
    def create_field(self, job_urlid, field_name, field_text,
                    name_is_operator_editable, text_is_operator_editable,
                    required_for_full_submission, field_has_been_set,
                    can_be_deleted, is_a_meta_field, submission_number
                    ):
        field = self.create(job=job_urlid, field_name=field_name,
                    field_text=field_text,
                    name_is_operator_editable=name_is_operator_editable,
                    text_is_operator_editable=text_is_operator_editable,
                    required_for_full_submission=required_for_full_submission,
                    field_has_been_set=field_has_been_set,
                    can_be_deleted=can_be_deleted,
                    is_a_meta_field=is_a_meta_field,
                    submission_number=submission_number
                    )
        return field


class Field(models.Model):
    job = models.CharField(max_length=36)
    field_name = models.CharField(max_length=100)
    field_text = models.CharField(max_length=200, blank=True)
    field_has_been_set = models.BooleanField(default=False)
    editing_mode = models.BooleanField(default=True)
    name_is_operator_editable = models.BooleanField(default=True)
    text_is_operator_editable = models.BooleanField(default=True)
    required_for_full_submission = models.BooleanField(default=True)
    can_be_deleted = models.BooleanField(default=True)
    is_a_meta_field = models.BooleanField(default=False)
    submission_number = models.CharField(default="1", max_length=5)

    objects = FieldManager()

    def __str__(self):
        return self.field_name


class JobInstructions(models.Model):
    jobid = models.CharField(db_column='jmpJobID',
                            max_length=20, primary_key=True
                            )
    instructions = models.TextField(db_column='jmpPartLongDescriptionText')

    class Meta:
        managed = False
        db_table = 'Jobs'

    def __str__(self):
        return self.jobid

class AssemblyInstructions(models.Model):
    jobid = models.CharField(db_column='jmaJobID',
                            max_length=20,
                            primary_key=True
                            )
    assemblyid = models.IntegerField(db_column='jmaJobAssemblyID')
    instructions = models.TextField(db_column='jmaPartLongDescriptionText')

    class Meta:
        managed = False
        db_table = 'JobAssemblies'

    def __str__(self):
        return self.jobid


class Notes(models.Model):
    job = models.CharField(max_length=36, unique=True)
    text = models.TextField()
