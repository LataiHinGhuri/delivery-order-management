from odoo import api, fields, models, _
from odoo.exceptions import UserError

class SaleOrder(models.Model):
    _inherit = "sale.order"



    @api.multi
    def action_confirm(self):
        self.ensure_one()
        res = super(SaleOrder, self).action_confirm()
        # raise UserError(_('Its working for sale to project.......')) 
        self.check_validtion()
        
        for order in self:
            
            self.create_task(order)
            # self.create_delivery_order(order)    
            
        return True
    ##################################
    #####mamun custom function for create task... 
    @api.multi
    def create_task(self,order):

        o_id=order.id
        
        # raise UserError(_('Its working.......'))
        config=self.env['del.order'].browse(1) 

        task = self.env['project.task'].create({
            'name': order.name,
            'partner_id': order.partner_id.id,
            'user_id': order.user_id.id,
            'description': order.name,
            'project_id': config.delivery_project_id,
            'stage_id': config.delivery_stage_id,
            'company_id': order.company_id.id,
            'x_order_id': o_id,
        })
        self.env.cr.commit()

    @api.multi
    def check_validtion(self):
        config=self.env['del.order'].browse(1)
        if config.delivery_project_id==0 or config.delivery_stage_id==0 or config.last_stage.id==0:
            raise UserError(_("Set Configuration for Delivery Order Management"))
        
        query="SELECT type_id FROM project_task_type_rel WHERE project_id=%s"
        param=(config.delivery_project_id,)
        self.env.cr.execute(query,param)
        # print(type_list)
        type_list = self.env.cr.dictfetchall()
        
        checker=0
        for typelist in type_list:
            # raise UserError(_(typelist['type_id']))
            if typelist['type_id']==config.delivery_stage_id or typelist['type_id']==config.last_stage.id:
                checker=checker+1

        if checker != 2:
            raise UserError(_("Set Configuration for Delivery Order Management"))

        # raise UserError(_(type_list[0]['type_id']))

        # raise UserError(_("Working wait"))
        return True
        

