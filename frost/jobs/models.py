import datetime
import uuid

from django.db import models
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.shortcuts import get_object_or_404

# Create your models here.
class Job(models.Model):
    jmojobid = models.CharField(db_column='jmoJobID', max_length=20)
    jmojobassemblyid = models.IntegerField(db_column='jmoJobAssemblyID')
    jmojoboperationid = models.IntegerField(db_column='jmoJobOperationID')
    jmooperationtype = models.DecimalField(db_column='jmoOperationType', max_digits=1, decimal_places=0)
    jmoaddedoperation = models.DecimalField(db_column='jmoAddedOperation', max_digits=1, decimal_places=0)
    jmoprototypeoperation = models.DecimalField(db_column='jmoPrototypeOperation', max_digits=1, decimal_places=0)
    jmoplantid = models.CharField(db_column='jmoPlantID', max_length=5)
    jmoplantdepartmentid = models.CharField(db_column='jmoPlantDepartmentID', max_length=5)
    jmoworkcenterid = models.CharField(db_column='jmoWorkCenterID', max_length=5)
    jmoprocessid = models.CharField(db_column='jmoProcessID', max_length=5)
    jmoprocessshortdescription = models.CharField(db_column='jmoProcessShortDescription', max_length=50)
    jmoprocesslongdescriptionrtf = models.TextField(db_column='jmoProcessLongDescriptionRTF')
    jmoprocesslongdescriptiontext = models.TextField(db_column='jmoProcessLongDescriptionText')
    jmoquantityperassembly = models.DecimalField(db_column='jmoQuantityPerAssembly', max_digits=13, decimal_places=6)
    jmosetuphours = models.DecimalField(db_column='jmoSetupHours', max_digits=8, decimal_places=2)
    jmoproductionstandard = models.DecimalField(db_column='jmoProductionStandard', max_digits=10, decimal_places=4)
    jmostandardfactor = models.CharField(db_column='jmoStandardFactor', max_length=2)
    jmosetuprate = models.DecimalField(db_column='jmoSetupRate', max_digits=8, decimal_places=2)
    jmoproductionrate = models.DecimalField(db_column='jmoProductionRate', max_digits=8, decimal_places=2)
    jmooverheadrate = models.DecimalField(db_column='jmoOverheadRate', max_digits=8, decimal_places=2)
    jmooperationquantity = models.DecimalField(db_column='jmoOperationQuantity', max_digits=15, decimal_places=5)
    jmoquantitycomplete = models.DecimalField(db_column='jmoQuantityComplete', max_digits=15, decimal_places=5)
    jmosetuppercentcomplete = models.DecimalField(db_column='jmoSetupPercentComplete', max_digits=3, decimal_places=0)
    jmoactualsetuphours = models.DecimalField(db_column='jmoActualSetupHours', max_digits=8, decimal_places=2)
    jmoactualproductionhours = models.DecimalField(db_column='jmoActualProductionHours', max_digits=8, decimal_places=2)
    jmosetupcomplete = models.DecimalField(db_column='jmoSetupComplete', max_digits=1, decimal_places=0)
    jmoproductioncomplete = models.DecimalField(db_column='jmoProductionComplete', max_digits=1, decimal_places=0)
    jmooverlap = models.DecimalField(db_column='jmoOverlap', max_digits=1, decimal_places=0)
    jmomachinetype = models.DecimalField(db_column='jmoMachineType', max_digits=1, decimal_places=0)
    jmoworkcentermachineid = models.DecimalField(db_column='jmoWorkCenterMachineID', max_digits=3, decimal_places=0)
    jmopartid = models.CharField(db_column='jmoPartID', max_length=30)
    jmopartrevisionid = models.CharField(db_column='jmoPartRevisionID', max_length=15)
    jmounitofmeasure = models.CharField(db_column='jmoUnitOfMeasure', max_length=2)
    jmosupplierorganizationid = models.CharField(db_column='jmoSupplierOrganizationID', max_length=10)
    jmopurchaselocationid = models.CharField(db_column='jmoPurchaseLocationID', max_length=5)
    jmofirm = models.DecimalField(db_column='jmoFirm', max_digits=1, decimal_places=0)
    jmopurchaseorderid = models.CharField(db_column='jmoPurchaseOrderID', max_length=10)
    jmoestimatedunitcost = models.DecimalField(db_column='jmoEstimatedUnitCost', max_digits=15, decimal_places=5)
    jmominimumcharge = models.DecimalField(db_column='jmoMinimumCharge', max_digits=8, decimal_places=2)
    jmosetupcharge = models.DecimalField(db_column='jmoSetupCharge', max_digits=9, decimal_places=2)
    jmocalculatedunitcost = models.DecimalField(db_column='jmoCalculatedUnitCost', max_digits=15, decimal_places=5)
    jmoquantitybreak1 = models.DecimalField(db_column='jmoQuantityBreak1', max_digits=15, decimal_places=5)
    jmounitcost1 = models.DecimalField(db_column='jmoUnitCost1', max_digits=15, decimal_places=5)
    jmoquantitybreak2 = models.DecimalField(db_column='jmoQuantityBreak2', max_digits=15, decimal_places=5)
    jmounitcost2 = models.DecimalField(db_column='jmoUnitCost2', max_digits=15, decimal_places=5)
    jmoquantitybreak3 = models.DecimalField(db_column='jmoQuantityBreak3', max_digits=15, decimal_places=5)
    jmounitcost3 = models.DecimalField(db_column='jmoUnitCost3', max_digits=15, decimal_places=5)
    jmoquantitybreak4 = models.DecimalField(db_column='jmoQuantityBreak4', max_digits=15, decimal_places=5)
    jmounitcost4 = models.DecimalField(db_column='jmoUnitCost4', max_digits=15, decimal_places=5)
    jmoquantitybreak5 = models.DecimalField(db_column='jmoQuantityBreak5', max_digits=15, decimal_places=5)
    jmounitcost5 = models.DecimalField(db_column='jmoUnitCost5', max_digits=15, decimal_places=5)
    jmoquantitybreak6 = models.DecimalField(db_column='jmoQuantityBreak6', max_digits=15, decimal_places=5)
    jmounitcost6 = models.DecimalField(db_column='jmoUnitCost6', max_digits=15, decimal_places=5)
    jmoquantitybreak7 = models.DecimalField(db_column='jmoQuantityBreak7', max_digits=15, decimal_places=5)
    jmounitcost7 = models.DecimalField(db_column='jmoUnitCost7', max_digits=15, decimal_places=5)
    jmoquantitybreak8 = models.DecimalField(db_column='jmoQuantityBreak8', max_digits=15, decimal_places=5)
    jmounitcost8 = models.DecimalField(db_column='jmoUnitCost8', max_digits=15, decimal_places=5)
    jmoquantitybreak9 = models.DecimalField(db_column='jmoQuantityBreak9', max_digits=15, decimal_places=5)
    jmounitcost9 = models.DecimalField(db_column='jmoUnitCost9', max_digits=15, decimal_places=5)
    jmostartdate = models.DateTimeField(db_column='jmoStartDate', blank=True, null=True)
    jmoduedate = models.DateTimeField(db_column='jmoDueDate', blank=True, null=True)
    jmostarthour = models.DecimalField(db_column='jmoStartHour', max_digits=5, decimal_places=2)
    jmoduehour = models.DecimalField(db_column='jmoDueHour', max_digits=5, decimal_places=2)
    jmoestimatedproductionhours = models.DecimalField(db_column='jmoEstimatedProductionHours', max_digits=8, decimal_places=2)
    jmocompletedsetuphours = models.DecimalField(db_column='jmoCompletedSetupHours', max_digits=8, decimal_places=2)
    jmocompletedproductionhours = models.DecimalField(db_column='jmoCompletedProductionHours', max_digits=8, decimal_places=2)
    jmodocuments = models.TextField(db_column='jmoDocuments')
    jmosfemessagertf = models.TextField(db_column='jmoSFEMessageRTF')
    jmosfemessagetext = models.TextField(db_column='jmoSFEMessageText')
    jmoclosed = models.DecimalField(db_column='jmoClosed', max_digits=1, decimal_places=0)
    jmoinspectioncomplete = models.DecimalField(db_column='jmoInspectionComplete', max_digits=1, decimal_places=0)
    jmoinspectionstatus = models.DecimalField(db_column='jmoInspectionStatus', max_digits=1, decimal_places=0)
    jmoinspectiontype = models.DecimalField(db_column='jmoInspectionType', max_digits=1, decimal_places=0)
    jmorfqid = models.CharField(db_column='jmoRFQID', max_length=10)
    jmocreatedby = models.CharField(db_column='jmoCreatedBy', max_length=20)
    jmocreateddate = models.DateTimeField(db_column='jmoCreatedDate', blank=True, null=True)
    jmouniqueid = models.CharField(db_column='jmoUniqueID', unique=True, max_length=36, editable=False, primary_key=True)
    ujmopriority = models.DecimalField(db_column='UJMOPRIORITY', max_digits=4, decimal_places=0)
    jmomachinestoschedule = models.DecimalField(db_column='jmoMachinesToSchedule', max_digits=3, decimal_places=0)

    class Meta:
        managed = False
        db_table = 'JobOperations'
        unique_together = (('jmojobid', 'jmojobassemblyid', 'jmojoboperationid'),)

    def __str__(self):
        return str(self.jmojobid) + " -- " + str(self.jmojobassemblyid) + " -- " + str(self.jmojoboperationid)


class FieldManager(models.Manager):
    def create_field(self, job_urlid, field_name, field_text, name_is_operator_editable, text_is_operator_editable, required_for_full_submission, field_has_been_set, can_be_deleted):
        job = Job.objects.filter(jmouniqueid__contains=job_urlid).extra({'jmouniqueid_uuid': "CAST(jmouniqueid as uniqueidentifier)"})[:1].get()
        field = self.create(job=job, field_name=field_name, field_text=field_text, name_is_operator_editable=name_is_operator_editable, text_is_operator_editable=text_is_operator_editable, required_for_full_submission=required_for_full_submission, field_has_been_set=field_has_been_set, can_be_deleted=can_be_deleted)
        return field


class Field(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, to_field='jmouniqueid')
    field_name = models.CharField(max_length=100)
    field_text = models.CharField(max_length=200, blank=True)
    field_has_been_set = models.BooleanField(default=False)
    editing_mode = models.BooleanField(default=False)
    name_is_operator_editable = models.BooleanField(default=True)
    text_is_operator_editable = models.BooleanField(default=True)
    required_for_full_submission = models.BooleanField(default=True)
    can_be_deleted = models.BooleanField(default=True)

    objects = FieldManager()

    def __str__(self):
        return self.field_name
