# -*- coding: utf-8 -*-

from odoo import api, fields, models


class ArmMenuGroup(models.Model):
    _name = 'arm.menu.group'
    _description = 'ARM Menu Hiding Group'
    _order = 'name, id'

    name = fields.Char(required=True, string='Group Name')
    active = fields.Boolean(default=True)
    note = fields.Text(string='Notes')

    user_ids = fields.Many2many(
        'res.users', 'arm_menu_group_user_rel', 'group_id', 'user_id', string='Users')
    hidden_menu_line_ids = fields.One2many(
        'arm.menu.group.line', 'group_id', string='Hidden Menus')

    @api.model
    def _runtime_active(self):
        return bool(
            getattr(self.env.registry, 'ready', True)
            and not self.env.su
            and self.env.uid != 1
            and not self.env.context.get('arm_bypass')
        )

    @api.model
    def _get_current_user_groups(self):
        if not self._runtime_active():
            return self.browse()
        return self.sudo().search([
            ('active', '=', True),
            ('user_ids', 'in', [self.env.uid]),
        ])

    @api.model
    def _clear_caches(self):
        self.env.registry.clear_cache()
        menu_model = self.env['ir.ui.menu']
        for method in ('clear_caches', 'clear_cache', '_clear_cache'):
            fn = getattr(menu_model, method, None)
            if fn:
                fn()
                break

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        self._clear_caches()
        return records

    def write(self, vals):
        res = super().write(vals)
        self._clear_caches()
        return res

    def unlink(self):
        res = super().unlink()
        self._clear_caches()
        return res


class ArmMenuGroupLine(models.Model):
    _name = 'arm.menu.group.line'
    _description = 'ARM Hidden Menu Line'
    _order = 'sequence, id'

    sequence = fields.Integer(default=10)
    group_id = fields.Many2one('arm.menu.group', required=True, ondelete='cascade')
    menu_id = fields.Many2one('ir.ui.menu', required=True, ondelete='cascade', string='Menu')

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        self.env['arm.menu.group']._clear_caches()
        return records

    def write(self, vals):
        res = super().write(vals)
        self.env['arm.menu.group']._clear_caches()
        return res

    def unlink(self):
        res = super().unlink()
        self.env['arm.menu.group']._clear_caches()
        return res
