from p import alias_and_resolve


def test_fallback_to_non_project_specific_command():
    assert 'p-new foo' == alias_and_resolve(
        cmd_name='p',
        cmd='p new foo',
        available_commands=['p-new'],
        cfg=dict(
            project_type='python',
            aliases={},
        )
    )

# This test causes an infinite loop in alias() right now
# def test_default():
#     assert 'p-run foo' == alias_and_resolve(
#         cmd_name='p',
#         cmd='p run',
#         available_commands=['p-pun'],
#         cfg=dict(
#             aliases={
#                 'p run': 'p run [foo]',
#             },
#         )
#     )


#
# def test_autodetect_c_sharp():  # .net generally?
#     assert 'c_sharp' == auto_detect_project_type(filenames=[
#     ])
#
#
# def test_autodetect_c():
#     assert 'c' == auto_detect_project_type(filenames=[
#     ])
#
#
# def test_autodetect_javascript():
#     assert 'javascript' == auto_detect_project_type(filenames=[
#     ])
#
#
# def test_autodetect_php():
#     assert 'php' == auto_detect_project_type(filenames=[
#     ])
#
#
# def test_autodetect_go():
#     assert 'go' == auto_detect_project_type(filenames=[
#     ])
