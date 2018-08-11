from django.db import models
from django.utils import timezone
from django.contrib.postgres.fields import JSONField
from django.contrib.postgres.fields import ArrayField

from cherry_note.users.models import User

class Tag(models.Model):
    name = models.CharField(verbose_name="Tag name", max_length=1024)

    def __str__(self):
        return self.name

class Note(models.Model):
    CUSTOM = 'CU'
    SIMPLE = 'SI'
    SYNTAX_CHOICES = (
        (CUSTOM, 'custom'),
        (SIMPLE, 'simple'),
    )

    name = models.CharField(verbose_name="Note name", max_length=1024)
    content = models.TextField(verbose_name="Note content", blank=True, default="")
    syntax = models.CharField(
        max_length=2, choices=SYNTAX_CHOICES,
        default=SIMPLE, blank=True, null=True,
    )
    is_read_only = models.BooleanField(verbose_name="Read only", default=False)
    has_code_box = models.BooleanField(verbose_name="Has code box", default=False)
    has_table = models.BooleanField(verbose_name="Has table", default=False)
    has_image = models.BooleanField(verbose_name="Has image", default=False)
    has_file = models.BooleanField(verbose_name="Has file", default=False)
    level = models.IntegerField(verbose_name="Level", blank=True, null=True, default=0)
    ts_created = models.DateTimeField(
        auto_now=True, verbose_name="Created",
    )
    ts_updated = models.DateTimeField(
        verbose_name="Updated",
        default=timezone.now
    )

    #tags = models.ManyToManyField(
    #    Tag, blank=True, null=True,
    #    related_name="notes",
    #    verbose_name="Tags"
    #)
    #tags = ArrayField(
    #    models.CharField(max_length=128, blank=True),
    #    default=[]
    #),
    tags = JSONField(verbose_name="Tags", blank=True, default=[])
    children = models.ManyToManyField(
        "self", blank=True, null=True,
        verbose_name="Child notes"
    )
    parent = models.ForeignKey(
        "self", on_delete=models.DO_NOTHING,
        blank=True, null=True,
        verbose_name="Parent note"
    )
    owner = models.ForeignKey(
        User, on_delete=models.DO_NOTHING,
        blank=True, null=True,
        verbose_name="Owner"
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('ts_created',)

class NoteInnerObject(models.Model):
    LEFT = 'LT'
    RIGHT = 'RT'
    CENTER = 'CR'
    JUSTIFICATION_CHOICES = (
        (LEFT, 'left'),
        (RIGHT, 'right'),
        (CENTER, 'center'),
    )

    note = models.ForeignKey(
        Note, on_delete=models.DO_NOTHING,
        verbose_name="Note"
    )
    offset = models.IntegerField(verbose_name="Offset", default=0)
    justification = models.CharField(
        max_length=2, choices=JUSTIFICATION_CHOICES,
        default=LEFT
    )

    class Meta:
        abstract = True

class CodeBox(NoteInnerObject):
    PYTHON2 = 'PY2'
    PYTHON3 = 'PY3'
    SYNTAX_CHOICES = (
        (PYTHON2, 'python2'),
        (PYTHON3, 'python3'),
    )

    code = models.TextField(verbose_name="Code", blank=True, default="")
    syntax = models.CharField(max_length=4, choices=SYNTAX_CHOICES)
    width = models.IntegerField(verbose_name="Width", default=700)
    height = models.IntegerField(verbose_name="Height", default=100)
    show_line_no = models.BooleanField(
        verbose_name="Show line numbers",
        default=False
    )

    def __str__(self):
        info = "{} {} length codebox".format(self.syntax, len(self.code))
        return info

class Table(NoteInnerObject):
    content = JSONField(verbose_name="Table content", blank=True, default={})

class File(NoteInnerObject):
    owner = models.ForeignKey(
        User, on_delete=models.DO_NOTHING,
        blank=True, null=True,
        verbose_name="Owner"
    )
    name = models.CharField(verbose_name="File name", max_length=1024)
    url = models.CharField(verbose_name="File URL", max_length=1024)
    size = models.IntegerField(verbose_name="Size", default=0)
    info = JSONField(verbose_name="Extra info", blank=True, default={})