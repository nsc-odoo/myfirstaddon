# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions

class Course(models.Model):  
	_name = 'test.course'
	_description = "Test course"

	title = fields.Char(string="Title", required=True)
	description = fields.Text()

	responsible_id = fields.Many2one('res.users', ondelete='set null', string="Responsible", index=True)
	session_ids     = fields.One2many(
		'test.session', 
		'course_id', 
		string="Sessions"
		)

	def copy(self, default=None):
		default = dict(default or {})
		
		copied_count = self.search_count(
			[('title', '=like', u"Copy of {}%".format(self.title))])
		if not copied_count:
			new_name = u"Copy of {}".format(self.title)
		else:
			new_name = u"Copy of {} ({})".format(self.title, copied_count)

		default['title'] = new_name
		return super(Course, self).copy(default)

	_sql_constraints =[
		('name_description_check',
		'CHECK(title != description)',
		"The title of the course should not be the description"),
		('name_unique',
        'UNIQUE(title)',
        "The course title must be unique"),
	]