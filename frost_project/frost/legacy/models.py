# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class Joboperations(models.Model):
    jmojobid = models.CharField(db_column='jmoJobID', max_length=20)  # Field name made lowercase.
    jmojobassemblyid = models.IntegerField(db_column='jmoJobAssemblyID')  # Field name made lowercase.
    jmojoboperationid = models.IntegerField(db_column='jmoJobOperationID')  # Field name made lowercase.
    jmooperationtype = models.DecimalField(db_column='jmoOperationType', max_digits=1, decimal_places=0)  # Field name made lowercase.
    jmoaddedoperation = models.DecimalField(db_column='jmoAddedOperation', max_digits=1, decimal_places=0)  # Field name made lowercase.
    jmoprototypeoperation = models.DecimalField(db_column='jmoPrototypeOperation', max_digits=1, decimal_places=0)  # Field name made lowercase.
    jmoplantid = models.CharField(db_column='jmoPlantID', max_length=5)  # Field name made lowercase.
    jmoplantdepartmentid = models.CharField(db_column='jmoPlantDepartmentID', max_length=5)  # Field name made lowercase.
    jmoworkcenterid = models.CharField(db_column='jmoWorkCenterID', max_length=5)  # Field name made lowercase.
    jmoprocessid = models.CharField(db_column='jmoProcessID', max_length=5)  # Field name made lowercase.
    jmoprocessshortdescription = models.CharField(db_column='jmoProcessShortDescription', max_length=50)  # Field name made lowercase.
    jmoprocesslongdescriptionrtf = models.TextField(db_column='jmoProcessLongDescriptionRTF')  # Field name made lowercase. This field type is a guess.
    jmoprocesslongdescriptiontext = models.TextField(db_column='jmoProcessLongDescriptionText')  # Field name made lowercase. This field type is a guess.
    jmoquantityperassembly = models.DecimalField(db_column='jmoQuantityPerAssembly', max_digits=13, decimal_places=6)  # Field name made lowercase.
    jmosetuphours = models.DecimalField(db_column='jmoSetupHours', max_digits=8, decimal_places=2)  # Field name made lowercase.
    jmoproductionstandard = models.DecimalField(db_column='jmoProductionStandard', max_digits=10, decimal_places=4)  # Field name made lowercase.
    jmostandardfactor = models.CharField(db_column='jmoStandardFactor', max_length=2)  # Field name made lowercase.
    jmosetuprate = models.DecimalField(db_column='jmoSetupRate', max_digits=8, decimal_places=2)  # Field name made lowercase.
    jmoproductionrate = models.DecimalField(db_column='jmoProductionRate', max_digits=8, decimal_places=2)  # Field name made lowercase.
    jmooverheadrate = models.DecimalField(db_column='jmoOverheadRate', max_digits=8, decimal_places=2)  # Field name made lowercase.
    jmooperationquantity = models.DecimalField(db_column='jmoOperationQuantity', max_digits=15, decimal_places=5)  # Field name made lowercase.
    jmoquantitycomplete = models.DecimalField(db_column='jmoQuantityComplete', max_digits=15, decimal_places=5)  # Field name made lowercase.
    jmosetuppercentcomplete = models.DecimalField(db_column='jmoSetupPercentComplete', max_digits=3, decimal_places=0)  # Field name made lowercase.
    jmoactualsetuphours = models.DecimalField(db_column='jmoActualSetupHours', max_digits=8, decimal_places=2)  # Field name made lowercase.
    jmoactualproductionhours = models.DecimalField(db_column='jmoActualProductionHours', max_digits=8, decimal_places=2)  # Field name made lowercase.
    jmosetupcomplete = models.DecimalField(db_column='jmoSetupComplete', max_digits=1, decimal_places=0)  # Field name made lowercase.
    jmoproductioncomplete = models.DecimalField(db_column='jmoProductionComplete', max_digits=1, decimal_places=0)  # Field name made lowercase.
    jmooverlap = models.DecimalField(db_column='jmoOverlap', max_digits=1, decimal_places=0)  # Field name made lowercase.
    jmomachinetype = models.DecimalField(db_column='jmoMachineType', max_digits=1, decimal_places=0)  # Field name made lowercase.
    jmoworkcentermachineid = models.DecimalField(db_column='jmoWorkCenterMachineID', max_digits=3, decimal_places=0)  # Field name made lowercase.
    jmopartid = models.CharField(db_column='jmoPartID', max_length=30)  # Field name made lowercase.
    jmopartrevisionid = models.CharField(db_column='jmoPartRevisionID', max_length=15)  # Field name made lowercase.
    jmounitofmeasure = models.CharField(db_column='jmoUnitOfMeasure', max_length=2)  # Field name made lowercase.
    jmosupplierorganizationid = models.CharField(db_column='jmoSupplierOrganizationID', max_length=10)  # Field name made lowercase.
    jmopurchaselocationid = models.CharField(db_column='jmoPurchaseLocationID', max_length=5)  # Field name made lowercase.
    jmofirm = models.DecimalField(db_column='jmoFirm', max_digits=1, decimal_places=0)  # Field name made lowercase.
    jmopurchaseorderid = models.CharField(db_column='jmoPurchaseOrderID', max_length=10)  # Field name made lowercase.
    jmoestimatedunitcost = models.DecimalField(db_column='jmoEstimatedUnitCost', max_digits=15, decimal_places=5)  # Field name made lowercase.
    jmominimumcharge = models.DecimalField(db_column='jmoMinimumCharge', max_digits=8, decimal_places=2)  # Field name made lowercase.
    jmosetupcharge = models.DecimalField(db_column='jmoSetupCharge', max_digits=9, decimal_places=2)  # Field name made lowercase.
    jmocalculatedunitcost = models.DecimalField(db_column='jmoCalculatedUnitCost', max_digits=15, decimal_places=5)  # Field name made lowercase.
    jmoquantitybreak1 = models.DecimalField(db_column='jmoQuantityBreak1', max_digits=15, decimal_places=5)  # Field name made lowercase.
    jmounitcost1 = models.DecimalField(db_column='jmoUnitCost1', max_digits=15, decimal_places=5)  # Field name made lowercase.
    jmoquantitybreak2 = models.DecimalField(db_column='jmoQuantityBreak2', max_digits=15, decimal_places=5)  # Field name made lowercase.
    jmounitcost2 = models.DecimalField(db_column='jmoUnitCost2', max_digits=15, decimal_places=5)  # Field name made lowercase.
    jmoquantitybreak3 = models.DecimalField(db_column='jmoQuantityBreak3', max_digits=15, decimal_places=5)  # Field name made lowercase.
    jmounitcost3 = models.DecimalField(db_column='jmoUnitCost3', max_digits=15, decimal_places=5)  # Field name made lowercase.
    jmoquantitybreak4 = models.DecimalField(db_column='jmoQuantityBreak4', max_digits=15, decimal_places=5)  # Field name made lowercase.
    jmounitcost4 = models.DecimalField(db_column='jmoUnitCost4', max_digits=15, decimal_places=5)  # Field name made lowercase.
    jmoquantitybreak5 = models.DecimalField(db_column='jmoQuantityBreak5', max_digits=15, decimal_places=5)  # Field name made lowercase.
    jmounitcost5 = models.DecimalField(db_column='jmoUnitCost5', max_digits=15, decimal_places=5)  # Field name made lowercase.
    jmoquantitybreak6 = models.DecimalField(db_column='jmoQuantityBreak6', max_digits=15, decimal_places=5)  # Field name made lowercase.
    jmounitcost6 = models.DecimalField(db_column='jmoUnitCost6', max_digits=15, decimal_places=5)  # Field name made lowercase.
    jmoquantitybreak7 = models.DecimalField(db_column='jmoQuantityBreak7', max_digits=15, decimal_places=5)  # Field name made lowercase.
    jmounitcost7 = models.DecimalField(db_column='jmoUnitCost7', max_digits=15, decimal_places=5)  # Field name made lowercase.
    jmoquantitybreak8 = models.DecimalField(db_column='jmoQuantityBreak8', max_digits=15, decimal_places=5)  # Field name made lowercase.
    jmounitcost8 = models.DecimalField(db_column='jmoUnitCost8', max_digits=15, decimal_places=5)  # Field name made lowercase.
    jmoquantitybreak9 = models.DecimalField(db_column='jmoQuantityBreak9', max_digits=15, decimal_places=5)  # Field name made lowercase.
    jmounitcost9 = models.DecimalField(db_column='jmoUnitCost9', max_digits=15, decimal_places=5)  # Field name made lowercase.
    jmostartdate = models.DateTimeField(db_column='jmoStartDate', blank=True, null=True)  # Field name made lowercase.
    jmoduedate = models.DateTimeField(db_column='jmoDueDate', blank=True, null=True)  # Field name made lowercase.
    jmostarthour = models.DecimalField(db_column='jmoStartHour', max_digits=5, decimal_places=2)  # Field name made lowercase.
    jmoduehour = models.DecimalField(db_column='jmoDueHour', max_digits=5, decimal_places=2)  # Field name made lowercase.
    jmoestimatedproductionhours = models.DecimalField(db_column='jmoEstimatedProductionHours', max_digits=8, decimal_places=2)  # Field name made lowercase.
    jmocompletedsetuphours = models.DecimalField(db_column='jmoCompletedSetupHours', max_digits=8, decimal_places=2)  # Field name made lowercase.
    jmocompletedproductionhours = models.DecimalField(db_column='jmoCompletedProductionHours', max_digits=8, decimal_places=2)  # Field name made lowercase.
    jmodocuments = models.TextField(db_column='jmoDocuments')  # Field name made lowercase. This field type is a guess.
    jmosfemessagertf = models.TextField(db_column='jmoSFEMessageRTF')  # Field name made lowercase. This field type is a guess.
    jmosfemessagetext = models.TextField(db_column='jmoSFEMessageText')  # Field name made lowercase. This field type is a guess.
    jmoclosed = models.DecimalField(db_column='jmoClosed', max_digits=1, decimal_places=0)  # Field name made lowercase.
    jmoinspectioncomplete = models.DecimalField(db_column='jmoInspectionComplete', max_digits=1, decimal_places=0)  # Field name made lowercase.
    jmoinspectionstatus = models.DecimalField(db_column='jmoInspectionStatus', max_digits=1, decimal_places=0)  # Field name made lowercase.
    jmoinspectiontype = models.DecimalField(db_column='jmoInspectionType', max_digits=1, decimal_places=0)  # Field name made lowercase.
    jmorfqid = models.CharField(db_column='jmoRFQID', max_length=10)  # Field name made lowercase.
    jmocreatedby = models.CharField(db_column='jmoCreatedBy', max_length=20)  # Field name made lowercase.
    jmocreateddate = models.DateTimeField(db_column='jmoCreatedDate', blank=True, null=True)  # Field name made lowercase.
    jmouniqueid = models.CharField(db_column='jmoUniqueID', unique=True, max_length=36, primary_key=True)  # Field name made lowercase.
    ujmopriority = models.DecimalField(db_column='UJMOPRIORITY', max_digits=4, decimal_places=0)  # Field name made lowercase.
    jmomachinestoschedule = models.DecimalField(db_column='jmoMachinesToSchedule', max_digits=3, decimal_places=0)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'JobOperations'
        unique_together = (('jmojobid', 'jmojobassemblyid', 'jmojoboperationid'),)

    def __str__(self):
        return str(self.jmojobid) + " -- " + str(self.jmojobassemblyid) + " -- " + str(self.jmojoboperationid)
