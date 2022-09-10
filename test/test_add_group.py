# -*- coding: utf-8 -*-

from model.group import Group


def test_add_group(app, db, json_test):
    group = json_test
    old_groups = db.get_group_list()
    app.group.create(group)
    new_groups = db.get_group_list()
    old_groups.append(group)
    assert sorted(old_groups, key=Group.id_or_max) == sorted(new_groups, key=Group.id_or_max)







