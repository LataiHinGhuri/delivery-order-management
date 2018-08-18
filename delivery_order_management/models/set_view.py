from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SetView(models.Model):
    _name = "set.view"

    @api.multi
    def activate_project_view(self):
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
