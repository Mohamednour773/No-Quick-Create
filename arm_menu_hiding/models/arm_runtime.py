# -*- coding: utf-8 -*-
import logging
from odoo import api, models, tools

_logger = logging.getLogger(__name__)


class ArmMenuHidingRuntime(models.Model):
    _inherit = 'ir.ui.menu'

    @api.model
    def _arm_hidden_menu_ids(self):
        group_model = self.env['arm.menu.group']
        if not group_model._runtime_active():
            return set()
        groups = group_model._get_current_user_groups()
        direct_ids = set(groups.hidden_menu_line_ids.mapped('menu_id').ids)
        if not direct_ids:
            return set()
        all_hidden = set(direct_ids)
        pending = set(direct_ids)
        while pending:
            children = set(self.sudo().search([('parent_id', 'in', list(pending))]).ids)
            children -= all_hidden
            if not children:
                break
            all_hidden.update(children)
            pending = children
        return all_hidden

    @api.model
    @tools.ormcache('self.env.uid', 'debug')
    def _visible_menu_ids(self, debug=False):
        visible = super()._visible_menu_ids(debug=debug)
        hidden = self._arm_hidden_menu_ids()
        if not hidden:
            return visible
        return set(visible) - hidden

    def _filter_visible_menus(self, *args, **kwargs):
        menus = super()._filter_visible_menus(*args, **kwargs)
        hidden = self._arm_hidden_menu_ids()
        if not hidden:
            return menus
        return menus.filtered(lambda m: m.id not in hidden)

    def load_menus(self, *args, **kwargs):
        result = super().load_menus(*args, **kwargs)
        hidden = self._arm_hidden_menu_ids()
        if not hidden or not isinstance(result, dict):
            return result

        if 'menus' in result:
            for mid in hidden:
                result['menus'].pop(str(mid), None)
                result['menus'].pop(mid, None)

        def _filter(node):
            if not isinstance(node, dict):
                return node
            if node.get('id') in hidden:
                return None
            if 'children' in node:
                node['children'] = [c for c in (_filter(ch) for ch in node['children']) if c]
            return node

        return _filter(result) or {'children': []}
