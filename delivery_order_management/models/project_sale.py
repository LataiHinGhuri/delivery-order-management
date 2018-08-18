from odoo import api, fields, models, _
from odoo.exceptions import UserError

class Task(models.Model):
    _inherit = "project.task"

    
    pid = 8

    @api.multi
    def write(self, vals):
        self.ensure_one()
        res = super(Task, self).write(vals)

        ####edit start... 
        if 'stage_id' in vals:
            # Here 11 is the stage id to change state to done for delivery
            config=self.env['del.order'].browse(1)
            stage_id_for_done_state = config.last_stage.id

            # raise UserError(_(stage_id_for_done_state))
            if vals['stage_id']==stage_id_for_done_state:

                
                #name needed to search stock picking id
                org=self.name

                #searching stock picking id for stock.picking database
                spid = self.env['stock.picking'].search([['origin', '=', org]])
                
                #collecting data from stoking picking using spid 
                sto_pic=self.env['stock.picking'].browse(spid.id)
                
                #If stock_picking state in confirmed state then we need to
                #force available first and then validate the order
                if sto_pic.state == 'confirmed':
                    sto_pic=self.env['stock.picking'].browse(spid.id)
                    
                    #make force available for all the product 
                    sto_pic.force_assign()

                    #make validate the order
                    st_done = self.env['stock.immediate.transfer'].create({'pick_id': spid.id})
                    st_done.process()

                #If stock_picking state in assigned state then we need to
                #validate the order dirrectly 
                elif sto_pic.state == 'assigned':
                    #createing object for stock.immediate.transfer class to call process methond
                    st_done = self.env['stock.immediate.transfer'].create({'pick_id': spid.id})
                    st_done.process()
######## edit done 


        # raise UserError(_('Delivery')) 
        