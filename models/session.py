# -*- coding: utf-8 -*-
from datetime import timedelta
from odoo import models, fields, api, exceptions

class Session(models.Model): 
	_name = 'test.session'
	_description = "Yoga Sessions"
	
	name = fields.Char(required=True)
	start_date = fields.Date(default=fields.Date.today)
	duration = fields.Float(digits=(6, 2), help="Duration in days")
	seats = fields.Integer(string="Number of seats")
	active = fields.Boolean("Actif", default=True)
	color=fields.Integer()
	
	instructor_id = fields.Many2one('res.partner',
		string="Instructor", 
		domain=['|', ('instructor','=',True), 
					('category_id.name','ilike',"Teacher")])
	
	course_id = fields.Many2one('test.course', 
		ondelete='cascade', 
		string="Course", 
		required=True
	)

	attendee_ids = fields.Many2many('res.partner',
		relation ='res_partner_test_session_rel',
		string="Attendees",
		domain=['!',('instructor','=',True)])

	#Computed fields
	fulliness = fields.Float(string="Pourcentage de remplitude", compute='_howmanypeoplewillcome')
	end_date = fields.Date(string="Date  de fin de la session", store=True, compute='_get_end_date', inverse='_set_end_date')
	attendees_count = fields.Integer(string="Attendees count", store=True, compute='_get_attendees_count')
	
	@api.depends('seats','attendee_ids')
	def _howmanypeoplewillcome(self):
		for item in self:
			if item.seats == 0:
				item.fulliness = 0.0
			else:
				item.fulliness = 100.0 * len(item.attendee_ids) / item.seats
	
	@api.depends('start_date','duration')
	def _get_end_date(self):
		for item in self:
			if not (item.start_date and item.duration):
				item.end_date = item.start_date
				continue
			# Add duration to start_date, but: Monday + 5 days = Saturday, so
			# subtract one second to get on Friday instead
			duration = timedelta(days=item.duration,seconds=0)
			item.end_date = item.start_date + duration

	def _set_end_date(self):
		for item in self:
			if not(item.start_date and item.end_date):
				continue
			item.duration =(item.end_date - item.start_date).days + 1 

	@api.onchange('seats', 'attendee_ids')
	def _validateSeats(self):
		if self.seats < 0:
			return {
				'warning':{
					'title': "Nombre de chaises incorrect",
					'message':"Le nombre ne peut pas etre negatif",
				},
			}
		if self.seats < len(self.attendee_ids):
			return {
				'warning':{
					'title':"Il y a beaucoup trop de monde!",
					'message':"Il faut virer du monde ou commander plus de chaise!",
				},
			}
	@api.depends('attendee_ids')
	def _get_attendees_count(self):
		for r in self:
			r.attendees_count = len(r.attendee_ids)

	@api.constrains('attendee_ids','instructor_id')
	def _cousetoyourselfnotallowed(self):
		for item in self:
			if item.instructor_id in item.attendee_ids:
				raise exceptions.ValidationError("On ne peut se donner cours à soit même")