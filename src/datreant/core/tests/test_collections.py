"""Tests for Bundle.

"""

import pytest

import datreant.core as dtr


def do_stuff(cont):
    return cont.name + cont.uuid


def return_nothing(cont):
    b = cont.name + cont.uuid


class CollectionsTests:
    """Mixin tests for collections"""
    pass


class TestView:
    """Tests for Views"""

    @pytest.fixture
    def collection(self):
        return dtr.View()

    def test_exists(self, collection, tmpdir):
        pass


class TestBundle:
    """Tests for common elements of Group.members and Bundle"""

    @pytest.fixture
    def collection(self):
        return dtr.Bundle()

    @pytest.fixture
    def testtreant(self, tmpdir, request):
        with tmpdir.as_cwd():
            t = dtr.Treant('dummytreant')
        return t

    @pytest.fixture
    def testgroup(self, tmpdir, request):
        with tmpdir.as_cwd():
            g = dtr.Group('dummygroup')
            g.members.add(dtr.Treant('bark'), dtr.Treant('leaf'))
        return g

    def test_additive(self, tmpdir, testtreant, testgroup, collection):
        """Test that addition of treants and collections give Bundles.

        """
        with tmpdir.as_cwd():
            assert isinstance(testtreant + testgroup, dtr.Bundle)
            assert len(testtreant + testgroup) == 2

            # subtle, but important; Group.members is a collection,
            # while Group is a treant
            assert len(testtreant + testgroup.members) != 2
            assert (len(testtreant + testgroup.members) ==
                    len(testgroup.members) + 1)

            assert isinstance(testtreant + testgroup.members, dtr.Bundle)

            b = collection + testtreant + testgroup

            # beating a dead horse
            assert len(b) == 2
            assert (len(b + testgroup.members) ==
                    len(b) + len(testgroup.members))
            assert isinstance(b + testgroup.members, dtr.Bundle)

    def test_subset(self, collection):
        pass

    def test_superset(self, collection):
        pass

    def test_difference(self, collection):
        pass

    def test_symmetric_difference(self, collection):
        pass

    def test_union(self, collection):
        pass

    def test_intersection(self, collection):
        pass

    def test_intersection(self, collection):
        pass

    def test_add_members(self, collection, tmpdir):
        """Try adding members in a number of ways"""
        with tmpdir.as_cwd():
            s1 = dtr.Treant('lark')
            s2 = dtr.Treant('hark')
            g3 = dtr.Group('linus')

            collection.add(s1, [g3, s2])

            for cont in (s1, s2, g3):
                assert cont in collection

            s4 = dtr.Treant('snoopy')
            collection.add([[s4], s2])
            assert s4 in collection

            # the group won't add members it alrady has
            # (operates as an ordered set)
            assert len(collection) == 4

    def test_add_members_glob(self, collection, tmpdir):
        """Try adding members with globbing"""
        with tmpdir.as_cwd():
            t1 = dtr.Treant('lark')
            t2 = dtr.Treant('hark')
            g3 = dtr.Group('linus')

            collection.add('*ark')

            for treant in (t1, t2):
                assert treant in collection

            assert g3 not in collection

    def test_get_members(self, collection, tmpdir):
        """Access members with indexing and slicing"""
        with tmpdir.as_cwd():
            s1 = dtr.Treant('larry')
            g2 = dtr.Group('curly')
            s3 = dtr.Treant('moe')

            collection.add([[[s1, [g2, [s3]]]]])

            assert collection[1] == g2

            c4 = dtr.treants.Treant('shemp')
            collection.add(c4)

            for member in (s1, g2, s3):
                assert member in collection[:3]

            assert c4 not in collection[:3]
            assert c4 == collection[-1]

    def test_fancy_index(self, collection):
        pass

    def test_name_index(self, collection):
        pass

    def test_uuid_index(self, collection):
        pass

    def test_remove_members(self, collection, tmpdir):
        """Try removing members"""
        with tmpdir.as_cwd():
            g1 = dtr.Group('lion-o')
            s2 = dtr.Treant('cheetara')
            s3 = dtr.Treant('snarf')

            collection.add(s3, g1, s2)

            for cont in (g1, s2, s3):
                assert cont in collection

            collection.remove(1)
            assert g1 not in collection

            collection.remove(s2)
            assert s2 not in collection

    def test_remove_members_name(self, collection, tmpdir):
        """Try removing members with names and globbing"""
        with tmpdir.as_cwd():
            t1 = dtr.Treant('lark')
            t2 = dtr.Treant('elsewhere/lark')
            t3 = dtr.Treant('hark')
            g = dtr.Group('linus')

            stuff = [t1, t2, t3, g]

            # test removal by name
            collection.add(stuff)
            for item in stuff:
                assert item in collection

            # should remove both treants with name 'lark'
            collection.remove('lark')

            for item in (t3, g):
                assert item in collection

            for item in (t1, t2):
                assert item not in collection

            # test removal by a unix-style glob pattern
            collection.add(stuff)
            for item in stuff:
                assert item in collection

            # should remove 'lark' and 'hark' treants
            collection.remove('*ark')

            assert g in collection

            for item in (t1, t2, t3):
                assert item not in collection

    def test_member_attributes(self, collection, tmpdir):
        """Get member uuids, names, and treanttypes"""
        with tmpdir.as_cwd():
            c1 = dtr.treants.Treant('bigger')
            g2 = dtr.Group('faster')
            s3 = dtr.Treant('stronger')

        collection.add(c1, g2, s3)

        uuids = [cont.uuid for cont in [c1, g2, s3]]
        assert collection.uuids == uuids

        names = [cont.name for cont in [c1, g2, s3]]
        assert collection.names == names

        treanttypes = [cont.treanttype for cont in [c1, g2, s3]]
        assert collection.treanttypes == treanttypes

    def test_map(self, collection, tmpdir):
        with tmpdir.as_cwd():
            s1 = dtr.Treant('lark')
            s2 = dtr.Treant('hark')
            g3 = dtr.Group('linus')

        collection.add(s1, s2, g3)

        comp = [cont.name + cont.uuid for cont in collection]
        assert collection.map(do_stuff) == comp
        assert collection.map(do_stuff, processes=2) == comp

        assert collection.map(return_nothing) is None
        assert collection.map(return_nothing, processes=2) is None

    def test_flatten(self, collection, tmpdir):
        """Test that flattening a collection of Treants and Groups works as
        expected.

        """
        treantnames = ('lark', 'mark', 'bark')
        with tmpdir.as_cwd():
            g = dtr.Group('bork')

            for name in treantnames:
                dtr.Treant(name)

            g.members.add('bork', *treantnames)

            # now our collection has a Group that has itself as a member
            # the flattened collection should detect this "loop" and leave
            # out the Group
            collection.add(g)

            assert len(collection) == 1

            b = collection.flatten()

            # shouldn't be any Groups
            assert g not in b

            # should have all our Treants
            assert len(b) == 3
            for name in treantnames:
                assert name in b.names

            # if we exclude the Group from the flattening, this should leave us
            # with nothing
            assert len(collection.flatten([g.uuid])) == 0

            # if one of the Treants is also a member of the collection,
            # should get something
            collection.add('mark')
            assert len(collection.flatten([g.uuid])) == 1
            assert 'mark' in collection.flatten([g.uuid]).names

    class TestAggTags:
        """Test behavior of manipulating tags collectively.

        """
        def test_add_tags(self, collection, testtreant, testgroup, tmpdir):
            with tmpdir.as_cwd():
                collection.add(testtreant, testgroup)

                assert len(collection.tags) == 0

                collection.tags.add('broiled', 'not baked')

                assert len(collection.tags) == 2
                for tag in ('broiled', 'not baked'):
                    assert tag in collection.tags

        def test_tags_setting(self, collection, testtreant, testgroup, tmpdir):
            pass

        def test_tags_all(self, collection, testtreant, testgroup, tmpdir):
            pass

        def test_tags_any(self, collection, testtreant, testgroup, tmpdir):
            pass

        def test_tags_any(self, collection, testtreant, testgroup, tmpdir):
            pass

        def test_tags_set_behavior(self, collection, testtreant, testgroup,
                                   tmpdir):
            pass

        def test_tags_getitem(self, collection, testtreant, testgroup, tmpdir):
            pass

        def test_tags_fuzzy(self, collection, testtreant, testgroup, tmpdir):
            pass

    class TestAggCategories:
        """Test behavior of manipulating categories collectively.

        """
        def test_add_categories(self, collection, testtreant, testgroup,
                                tmpdir):
            with tmpdir.as_cwd():
                # add a test Treant and a test Group to collection
                collection.add(testtreant, testgroup)
                assert len(collection.categories) == 0

                # add 'age' and 'bark' as categories of this collection
                collection.categories.add({'age': 42}, bark='smooth')
                assert len(collection.categories) == 2

                for member in collection:
                    assert member.categories['age'] == 42
                    assert member.categories['bark'] == 'smooth'
                for key in ['age', 'bark']:
                    assert key in collection.categories.any

                t1 = dtr.Treant('hickory')
                t1.categories.add(bark='shaggy', species='ovata')
                collection.add(t1)
                assert len(collection.categories) == 1
                assert len(collection.categories.all) == 1
                assert len(collection.categories.any) == 3

                collection.categories.add(location='USA')
                assert len(collection.categories) == 2
                assert len(collection.categories.all) == 2
                assert len(collection.categories.any) == 4
                for member in collection:
                    assert member.categories['location'] == 'USA'

        def test_categories_getitem(self, collection, testtreant, testgroup,
                                    tmpdir):
            with tmpdir.as_cwd():
                # add a test Treant and a test Group to collection
                collection.add(testtreant, testgroup)
                # add 'age' and 'bark' as categories of this collection
                collection.categories.add({'age': 42, 'bark': 'smooth'})

                t1 = dtr.Treant('maple')
                t2 = dtr.Treant('sequoia')
                t1.categories.add({'age': 'seedling', 'bark': 'rough',
                                   'type': 'deciduous'})
                t2.categories.add({'age': 'adult', 'bark': 'rough',
                                   'type': 'evergreen', 'nickname': 'redwood'})
                collection.add(t1, t2)
                assert len(collection.categories) == 2
                assert len(collection.categories.any) == 4

                # test values for each category in the collection
                age_list = [42, 42, 'seedling', 'adult']
                assert age_list == collection.categories['age']
                bark_list = ['smooth', 'smooth', 'rough', 'rough']
                assert bark_list == collection.categories['bark']
                type_list = [None, None, 'deciduous', 'evergreen']
                assert type_list == collection.categories['type']
                nick_list = [None, None,  None, 'redwood']
                assert nick_list == collection.categories['nickname']

                # test list of keys as input
                cat_list = [age_list, type_list]
                assert cat_list == collection.categories[['age', 'type']]

                # test set of keys as input
                cat_set = {'bark': bark_list, 'nickname': nick_list}
                assert cat_set == collection.categories[{'bark', 'nickname'}]

        def test_categories_setitem(self, collection, testtreant, testgroup,
                                    tmpdir):
            with tmpdir.as_cwd():
                # add a test Treant and a test Group to collection
                collection.add(testtreant, testgroup)
                # add 'age' and 'bark' as categories of this collection
                collection.categories.add({'age': 42, 'bark': 'smooth'})

                t1 = dtr.Treant('maple')
                t2 = dtr.Treant('sequoia')
                t1.categories.add({'age': 'seedling', 'bark': 'rough',
                                   'type': 'deciduous'})
                t2.categories.add({'age': 'adult', 'bark': 'rough',
                                   'type': 'evergreen', 'nickname': 'redwood'})
                collection.add(t1, t2)

                # test setting a category when all members have it
                for value in collection.categories['age']:
                    assert value in [42, 42, 'seedling', 'adult']
                collection.categories['age'] = 'old'
                for value in collection.categories['age']:
                    assert value in ['old', 'old', 'old', 'old']

                # test setting a new category (no members have it)
                assert 'location' not in collection.categories.any
                collection.categories['location'] = 'USA'
                for value in collection.categories['location']:
                    assert value in ['USA', 'USA', 'USA', 'USA']

                # test setting a category that only some members have
                assert 'nickname' in collection.categories.any
                assert 'nickname' not in collection.categories.all
                collection.categories['nickname'] = 'friend'
                for value in collection.categories['nickname']:
                    assert value in ['friend', 'friend', 'friend', 'friend']

                # test setting values for individual members
                assert 'favorite ice cream' not in collection.categories
                ice_creams = ['rocky road',
                              'americone dream',
                              'moose tracks',
                              'vanilla']
                collection.categories['favorite ice cream'] = ice_creams

                for member, ice_cream in zip(collection, ice_creams):
                    assert member.categories['favorite ice cream'] == ice_cream

        def test_categories_all(self, collection, testtreant, testgroup,
                                tmpdir):
            with tmpdir.as_cwd():
                # add a test Treant and a test Group to collection
                collection.add(testtreant, testgroup)
                # add 'age' and 'bark' as categories of this collection
                collection.categories.add({'age': 42}, bark='bare')

                # add categories to 'hickory' Treant, then add to collection
                t1 = dtr.Treant('hickory')
                t1.categories.add(bark='shaggy', species='ovata')
                collection.add(t1)
                # check the contents of 'bark', ensure 'age' and 'species' are
                # not shared categories of the collection
                collection.add(t1)
                common_categories = collection.categories.all
                assert len(collection.categories) == len(common_categories)
                assert 'age' not in common_categories
                assert 'species' not in common_categories
                assert common_categories['bark'] == ['bare', 'bare', 'shaggy']

                # add 'location' category to collection
                collection.categories.add(location='USA')
                common_categories = collection.categories.all
                # ensure all members have 'USA' for their 'location'
                assert len(collection.categories) == len(common_categories)
                assert 'age' not in common_categories
                assert 'species' not in common_categories
                assert common_categories['bark'] == ['bare', 'bare', 'shaggy']
                assert common_categories['location'] == ['USA', 'USA', 'USA']

                # add 'location' category to collection
                collection.categories.remove('bark')
                common_categories = collection.categories.all
                # check that only 'location' is a shared category
                assert len(collection.categories) == len(common_categories)
                assert 'age' not in common_categories
                assert 'bark' not in common_categories
                assert 'species' not in common_categories
                assert common_categories['location'] == ['USA', 'USA', 'USA']

        def test_categories_any(self, collection, testtreant, testgroup,
                                tmpdir):
            with tmpdir.as_cwd():
                # add a test Treant and a test Group to collection
                collection.add(testtreant, testgroup)
                # add 'age' and 'bark' as categories of this collection
                collection.categories.add({'age': 42}, bark='smooth')
                assert len(collection.categories.any) == 2

                # add categories to 'hickory' Treant, then add to collection
                t1 = dtr.Treant('hickory')
                t1.categories.add(bark='shaggy', species='ovata')
                collection.add(t1)
                # check the contents of 'bark', ensure 'age' and 'species' are
                # not shared categories of the collection
                every_category = collection.categories.any
                assert len(every_category) == 3
                assert every_category['age'] == [42, 42, None]
                assert every_category['bark'] == ['smooth', 'smooth', 'shaggy']
                assert every_category['species'] == [None, None, 'ovata']

                # add 'location' category to collection
                collection.categories.add(location='USA')
                every_category = collection.categories.any
                # ensure all members have 'USA' for their 'location'
                assert len(every_category) == 4
                assert every_category['age'] == [42, 42, None]
                assert every_category['bark'] == ['smooth', 'smooth', 'shaggy']
                assert every_category['species'] == [None, None, 'ovata']
                assert every_category['location'] == ['USA', 'USA', 'USA']

                # add 'sprout' to 'age' category of 'hickory' Treant
                t1.categories['age'] = 'sprout'
                every_category = collection.categories.any
                # check 'age' is category for 'hickory' and is 'sprout'
                assert len(every_category) == 4
                assert every_category['age'] == [42, 42, 'sprout']
                assert every_category['bark'] == ['smooth', 'smooth', 'shaggy']
                assert every_category['species'] == [None, None, 'ovata']
                assert every_category['location'] == ['USA', 'USA', 'USA']

                # add 'location' category to collection
                collection.categories.remove('bark')
                every_category = collection.categories.any
                # check that only 'location' is a shared category
                assert len(every_category) == 3
                assert every_category['age'] == [42, 42, 'sprout']
                assert every_category['species'] == [None, None, 'ovata']
                assert every_category['location'] == ['USA', 'USA', 'USA']
                assert 'bark' not in every_category

        def test_categories_remove(self, collection, testtreant, testgroup,
                                   tmpdir):
            with tmpdir.as_cwd():
                t1 = dtr.Treant('maple')
                t2 = dtr.Treant('sequoia')
                collection.add(t1, t2)
                collection.categories.add({'age': 'sprout'}, bark='rough')

                collection.add(testtreant, testgroup)
                assert len(collection.categories) == 0
                assert len(collection.categories.any) == 2

                # add 'USA', ensure 'location', 'age', 'bark' is a category in
                # at least one of the members
                collection.categories.add(location='USA')
                assert len(collection.categories) == 1
                for key in ['location', 'age', 'bark']:
                    assert key in collection.categories.any
                # ensure 'age' and 'bark' are each not categories for all
                # members in collection
                assert 'age' not in collection.categories
                assert 'bark' not in collection.categories

                # remove 'bark', test for any instance of 'bark' in the
                # collection
                collection.categories.remove('bark')
                assert len(collection.categories) == 1
                for key in ['location', 'age']:
                    assert key in collection.categories.any
                assert 'bark' not in collection.categories.any

                # remove 'age', test that 'age' is not a category for any
                # member in collection
                collection.categories.remove('age')
                for member in collection:
                    assert 'age' not in member.categories
                # test that 'age' is not a category of this collection
                assert 'age' not in collection.categories.any

        def test_categories_keys(self, collection, testtreant, testgroup,
                                 tmpdir):
            with tmpdir.as_cwd():
                collection.add(testtreant, testgroup)
                collection.categories.add({'age': 42, 'bark': 'smooth'})

                t1 = dtr.Treant('maple')
                t2 = dtr.Treant('sequoia')
                t1.categories.add({'age': 'seedling', 'bark': 'rough',
                                   'type': 'deciduous'})
                t2.categories.add({'age': 'adult', 'bark': 'rough',
                                   'type': 'evergreen', 'nickname': 'redwood'})
                collection.add(t1, t2)

                for k in collection.categories.keys(scope='all'):
                    for member in collection:
                        assert k in member.categories

                for k in collection.categories.keys(scope='any'):
                    for member in collection:
                        if k == 'nickname':
                            if member.name == 'maple':
                                assert k not in member.categories
                            elif member.name == 'sequoia':
                                assert k in member.categories
                        elif k == 'type':
                            if (member.name != 'maple' and
                                    member.name != 'sequoia'):
                                assert k not in member.categories

                        else:
                            assert k in member.categories

        def test_categories_values(self, collection, testtreant, testgroup,
                                   tmpdir):
            with tmpdir.as_cwd():
                collection.add(testtreant, testgroup)
                collection.categories.add({'age': 'young', 'bark': 'smooth'})

                t1 = dtr.Treant('maple')
                t2 = dtr.Treant('sequoia')
                t1.categories.add({'age': 'seedling', 'bark': 'rough',
                                   'type': 'deciduous'})
                t2.categories.add({'age': 'adult', 'bark': 'rough',
                                   'type': 'evergreen', 'nickname': 'redwood'})
                collection.add(t1, t2)

                for scope in ('all', 'any'):
                    for i, v in enumerate(
                            collection.categories.values(scope=scope)):
                        assert v == collection.categories[
                                collection.categories.keys(scope=scope)[i]]

        def test_categories_groupby(self, collection, testtreant, testgroup,
                                    tmpdir):
            with tmpdir.as_cwd():
                t1 = dtr.Treant('maple')
                t2 = dtr.Treant('sequoia')
                t3 = dtr.Treant('elm')
                t4 = dtr.Treant('oak')
                t1.categories.add({'age': 'young', 'bark': 'smooth',
                                   'type': 'deciduous'})
                t2.categories.add({'age': 'adult', 'bark': 'fibrous',
                                   'type': 'evergreen', 'nickname': 'redwood'})
                t3.categories.add({'age': 'old', 'bark': 'mossy',
                                   'type': 'deciduous', 'health': 'poor'})
                t4.categories.add({'age': 'young', 'bark': 'mossy',
                                   'type': 'deciduous', 'health': 'good'})
                collection.add(t1, t2, t3, t4)

                age_group = collection.categories.groupby('age')
                assert {t1, t4} == set(age_group['young'])
                assert {t2} == set(age_group['adult'])
                assert {t3} == set(age_group['old'])

                bark_group = collection.categories.groupby('bark')
                assert {t1} == set(bark_group['smooth'])
                assert {t2} == set(bark_group['fibrous'])
                assert {t3, t4} == set(bark_group['mossy'])

                type_group = collection.categories.groupby('type')
                assert {t1, t3, t4} == set(type_group['deciduous'])
                assert {t2} == set(type_group['evergreen'])

                nick_group = collection.categories.groupby('nickname')
                assert {t2} == set(nick_group['redwood'])
                for bundle in nick_group.values():
                    assert {t1, t3, t4}.isdisjoint(set(bundle))

                health_group = collection.categories.groupby('health')
                assert {t3} == set(health_group['poor'])
                assert {t4} == set(health_group['good'])
                for bundle in health_group.values():
                    assert {t1, t2}.isdisjoint(set(bundle))

                # test list of keys as input
                age_bark = collection.categories.groupby(['age', 'bark'])
                assert len(age_bark) == 4
                assert {t1} == set(age_bark[('young', 'smooth')])
                assert {t2} == set(age_bark[('adult', 'fibrous')])
                assert {t3} == set(age_bark[('old', 'mossy')])
                assert {t4} == set(age_bark[('young', 'mossy')])

                age_bark = collection.categories.groupby({'age', 'bark'})
                assert len(age_bark) == 4
                assert {t1} == set(age_bark[('young', 'smooth')])
                assert {t2} == set(age_bark[('adult', 'fibrous')])
                assert {t3} == set(age_bark[('old', 'mossy')])
                assert {t4} == set(age_bark[('young', 'mossy')])

                type_health = collection.categories.groupby(['type', 'health'])
                assert len(type_health) == 2
                assert {t3} == set(type_health[('poor', 'deciduous')])
                assert {t4} == set(type_health[('good', 'deciduous')])
                for bundle in type_health.values():
                    assert {t1, t2}.isdisjoint(set(bundle))

                type_health = collection.categories.groupby(['health', 'type'])
                assert len(type_health) == 2
                assert {t3} == set(type_health[('poor', 'deciduous')])
                assert {t4} == set(type_health[('good', 'deciduous')])
                for bundle in type_health.values():
                    assert {t1, t2}.isdisjoint(set(bundle))

                age_nick = collection.categories.groupby(['age', 'nickname'])
                assert len(age_nick) == 1
                assert {t2} == set(age_nick['adult', 'redwood'])
                for bundle in age_nick.values():
                    assert {t1, t3, t4}.isdisjoint(set(bundle))

                keys = ['age', 'bark', 'health']
                age_bark_health = collection.categories.groupby(keys)
                assert len(age_bark_health) == 2
                assert {t3} == set(age_bark_health[('old', 'mossy', 'poor')])
                assert {t4} == set(age_bark_health[('young', 'mossy', 'good')])
                for bundle in age_bark_health.values():
                    assert {t1, t2}.isdisjoint(set(bundle))

                keys = ['age', 'bark', 'type', 'nickname']
                abtn = collection.categories.groupby(keys)
                assert len(abtn) == 1
                assert {t2} == set(abtn[('adult', 'fibrous', 'redwood',
                                         'evergreen')])
                for bundle in abtn.values():
                    assert {t1, t3, t4}.isdisjoint(set(bundle))

                keys = ['bark', 'nickname', 'type', 'age']
                abtn2 = collection.categories.groupby(keys)
                assert len(abtn2) == 1
                assert {t2} == set(abtn2[('adult', 'fibrous', 'redwood',
                                          'evergreen')])
                for bundle in abtn2.values():
                    assert {t1, t3, t4}.isdisjoint(set(bundle))

                keys = {'age', 'bark', 'type', 'nickname'}
                abtn_set = collection.categories.groupby(keys)
                assert len(abtn_set) == 1
                assert {t2} == set(abtn_set[('adult', 'fibrous', 'redwood',
                                             'evergreen')])
                for bundle in abtn_set.values():
                    assert {t1, t3, t4}.isdisjoint(set(bundle))

                keys = ['health', 'nickname']
                health_nick = collection.categories.groupby(keys)
                assert len(health_nick) == 0
                for bundle in health_nick.values():
                    assert {t1, t2, t3, t4}.isdisjoint(set(bundle))
