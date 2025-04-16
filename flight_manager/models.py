# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Airline(models.Model):
    airlineid = models.CharField(db_column='airlineID', primary_key=True, max_length=50)  # Field name made lowercase.
    revenue = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'airline'


class Airplane(models.Model):
    airlineid = models.OneToOneField(Airline, models.DO_NOTHING, db_column='airlineID', primary_key=True)  # Field name made lowercase. The composite primary key (airlineID, tail_num) found, that is not supported. The first column is selected.
    tail_num = models.CharField(max_length=50, unique=True)
    seat_capacity = models.IntegerField()
    speed = models.IntegerField()
    locationid = models.ForeignKey('Location', models.DO_NOTHING, db_column='locationID', blank=True, null=True)  # Field name made lowercase.
    plane_type = models.CharField(max_length=100, blank=True, null=True)
    maintenanced = models.IntegerField(blank=True, null=True)
    model = models.CharField(max_length=50, blank=True, null=True)
    neo = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'airplane'
        unique_together = (('airlineid', 'tail_num'),)


class Airport(models.Model):
    airportid = models.CharField(db_column='airportID', primary_key=True, max_length=3)  # Field name made lowercase.
    airport_name = models.CharField(max_length=200, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=3)
    locationid = models.ForeignKey('Location', models.DO_NOTHING, db_column='locationID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'airport'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Flight(models.Model):
    flightid = models.CharField(db_column='flightID', primary_key=True, max_length=50)  # Field name made lowercase.
    routeid = models.ForeignKey('Route', models.DO_NOTHING, db_column='routeID')  # Field name made lowercase.
    support_airline = models.ForeignKey(Airplane, models.DO_NOTHING, db_column='support_airline', blank=True, null=True)
    support_tail = models.ForeignKey(Airplane, models.DO_NOTHING, db_column='support_tail', to_field='tail_num', related_name='flight_support_tail_set', blank=True, null=True, unique=True)
    progress = models.IntegerField(blank=True, null=True)
    airplane_status = models.CharField(max_length=100, blank=True, null=True)
    next_time = models.TimeField(blank=True, null=True)
    cost = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'flight'


class Leg(models.Model):
    legid = models.CharField(db_column='legID', primary_key=True, max_length=50)  # Field name made lowercase.
    departure = models.ForeignKey(Airport, models.DO_NOTHING, db_column='departure')
    arrival = models.ForeignKey(Airport, models.DO_NOTHING, db_column='arrival', related_name='leg_arrival_set')
    distance = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'leg'


class Location(models.Model):
    locationid = models.CharField(db_column='locationID', primary_key=True, max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'location'


class Magic44AutogradingHighLevel(models.Model):
    score_tag = models.CharField(max_length=1, blank=True, null=True)
    score_category = models.CharField(max_length=100, blank=True, null=True)
    total_possible = models.DecimalField(max_digits=42, decimal_places=0, blank=True, null=True)
    total_passed = models.DecimalField(max_digits=42, decimal_places=0, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'magic44_autograding_high_level'


class Magic44AutogradingLowLevel(models.Model):
    query_label = models.CharField(max_length=20, blank=True, null=True)
    query_name = models.CharField(max_length=100, blank=True, null=True)
    total_cases = models.BigIntegerField()
    passed_cases = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'magic44_autograding_low_level'


class Magic44AutogradingQueryLevel(models.Model):
    query_status_category = models.CharField(max_length=1000, blank=True, null=True)
    number_affected = models.BigIntegerField(blank=True, null=True)
    queries_affected = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'magic44_autograding_query_level'


class Magic44AutogradingScoreSummary(models.Model):
    query_label = models.CharField(max_length=20, blank=True, null=True)
    query_name = models.CharField(max_length=100, blank=True, null=True)
    final_score = models.DecimalField(max_digits=55, decimal_places=2, blank=True, null=True)
    scoring_weight = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'magic44_autograding_score_summary'


class Magic44ColumnErrors(models.Model):
    query_id = models.IntegerField(blank=True, null=True)
    step_id = models.IntegerField()
    category = models.CharField(max_length=7)
    row_hash = models.TextField()

    class Meta:
        managed = False
        db_table = 'magic44_column_errors'


class Magic44DataCapture(models.Model):
    stepid = models.IntegerField(db_column='stepID', blank=True, null=True)  # Field name made lowercase.
    queryid = models.IntegerField(db_column='queryID', blank=True, null=True)  # Field name made lowercase.
    columndump0 = models.CharField(db_column='columnDump0', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    columndump1 = models.CharField(db_column='columnDump1', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    columndump2 = models.CharField(db_column='columnDump2', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    columndump3 = models.CharField(db_column='columnDump3', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    columndump4 = models.CharField(db_column='columnDump4', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    columndump5 = models.CharField(db_column='columnDump5', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    columndump6 = models.CharField(db_column='columnDump6', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    columndump7 = models.CharField(db_column='columnDump7', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    columndump8 = models.CharField(db_column='columnDump8', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    columndump9 = models.CharField(db_column='columnDump9', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    columndump10 = models.CharField(db_column='columnDump10', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    columndump11 = models.CharField(db_column='columnDump11', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    columndump12 = models.CharField(db_column='columnDump12', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    columndump13 = models.CharField(db_column='columnDump13', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    columndump14 = models.CharField(db_column='columnDump14', max_length=1000, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'magic44_data_capture'


class Magic44ExpectedResults(models.Model):
    step_id = models.IntegerField()
    query_id = models.IntegerField(blank=True, null=True)
    row_hash = models.CharField(max_length=2000)

    class Meta:
        managed = False
        db_table = 'magic44_expected_results'


class Magic44LogQueryErrors(models.Model):
    step_id = models.IntegerField(blank=True, null=True)
    query_id = models.IntegerField(blank=True, null=True)
    query_text = models.CharField(max_length=2000, blank=True, null=True)
    error_code = models.CharField(max_length=5, blank=True, null=True)
    error_message = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'magic44_log_query_errors'


class Magic44RowCountErrors(models.Model):
    query_id = models.IntegerField(blank=True, null=True)
    step_id = models.IntegerField()
    answer_total = models.BigIntegerField(blank=True, null=True)
    result_total = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'magic44_row_count_errors'


class Magic44TableNameLookup(models.Model):
    query_id = models.IntegerField(primary_key=True)
    table_or_view_name = models.CharField(max_length=2000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'magic44_table_name_lookup'


class Magic44TestCaseDirectory(models.Model):
    base_step_id = models.IntegerField(blank=True, null=True)
    number_of_steps = models.IntegerField(blank=True, null=True)
    query_label = models.CharField(max_length=20, blank=True, null=True)
    query_name = models.CharField(max_length=100, blank=True, null=True)
    scoring_weight = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'magic44_test_case_directory'


class Magic44TestResults(models.Model):
    step_id = models.IntegerField()
    query_id = models.IntegerField(blank=True, null=True)
    row_hash = models.CharField(max_length=2000)

    class Meta:
        managed = False
        db_table = 'magic44_test_results'


class Passenger(models.Model):
    personid = models.OneToOneField('Person', models.DO_NOTHING, db_column='personID', primary_key=True)  # Field name made lowercase.
    miles = models.IntegerField(blank=True, null=True)
    funds = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'passenger'


class PassengerVacations(models.Model):
    personid = models.OneToOneField('Person', models.DO_NOTHING, db_column='personID', primary_key=True)  # Field name made lowercase. The composite primary key (personID, sequence) found, that is not supported. The first column is selected.
    airportid = models.ForeignKey(Airport, models.DO_NOTHING, db_column='airportID')  # Field name made lowercase.
    sequence = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'passenger_vacations'
        unique_together = (('personid', 'sequence'),)


class Person(models.Model):
    personid = models.CharField(db_column='personID', primary_key=True, max_length=50)  # Field name made lowercase.
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    locationid = models.ForeignKey(Location, models.DO_NOTHING, db_column='locationID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'person'


class Pilot(models.Model):
    personid = models.OneToOneField(Person, models.DO_NOTHING, db_column='personID', primary_key=True)  # Field name made lowercase.
    taxid = models.CharField(db_column='taxID', unique=True, max_length=50)  # Field name made lowercase.
    experience = models.IntegerField(blank=True, null=True)
    commanding_flight = models.ForeignKey(Flight, models.DO_NOTHING, db_column='commanding_flight', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pilot'


class PilotLicenses(models.Model):
    personid = models.OneToOneField(Pilot, models.DO_NOTHING, db_column='personID', primary_key=True)  # Field name made lowercase. The composite primary key (personID, license) found, that is not supported. The first column is selected.
    license = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'pilot_licenses'
        unique_together = (('personid', 'license'),)


class Route(models.Model):
    routeid = models.CharField(db_column='routeID', primary_key=True, max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'route'


class RoutePath(models.Model):
    routeid = models.OneToOneField(Route, models.DO_NOTHING, db_column='routeID', primary_key=True)  # Field name made lowercase. The composite primary key (routeID, sequence) found, that is not supported. The first column is selected.
    legid = models.ForeignKey(Leg, models.DO_NOTHING, db_column='legID')  # Field name made lowercase.
    sequence = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'route_path'
        unique_together = (('routeid', 'sequence'),)
