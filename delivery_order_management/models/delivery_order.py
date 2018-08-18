from odoo import api, models, fields, _
from odoo.exceptions import UserError,Warning


class del_order(models.Model):
    _name='del.order'


    config_state = fields.Boolean(string="State", default=False)
    delivery_project_id = fields.Integer(string="Project Id")
    delivery_stage_id = fields.Integer(string="Stage Id")
    delivery_project_name = fields.Char(string="Project")
    delivery_stage_name = fields.Char(string="Stage")

    # selected_project = fields.Many2one('account.analytic.account', string="Project Name")
    selected_project = fields.Many2one(
        'project.project', 'Project', company_dependent=True, required=True,
        help='Create a task under this project on sale order validation. This setting must be set for each company.')
    selected_stage = fields.Many2one('project.task.type', string="First Stage", required=True,)
    last_stage = fields.Many2one('project.task.type', string="Last Stage", required=True,)

    @api.model
    def dele(self):
        if (self.selected_stage.id):
            pass
            stageid=self.selected_stage.id
            projectid=self.selected_project.id
            laststage=self.last_stage.id

            query="UPDATE del_order SET delivery_stage_id=%s,delivery_project_id=%s, last_stage=%s WHERE id=%s"
            param=(stageid,projectid,laststage,1,)
            self.env.cr.execute(query,param)
            
            return True

        # raise UserError(_(query))
    @api.multi   
    def button_action(self):
        self.dele()
        # raise Warning(_(str(self.dele())))

        config = self.env['del.order'].browse(1)
        pid = config.delivery_project_id

        view = self.env.ref('project.view_task_kanban')

        # TDE FIXME: a return in a loop, what a good idea. Really.
        return {
                'name': _('Delivery Order Management'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'kanban',
                'res_model': 'project.task',
                'views': [(view.id, 'kanban')],
                'view_id': view.id,
                'context': {'group_by': 'stage_id','search_default_project_id': [pid],'default_project_id': pid,},
        }
        
        
    
     


    