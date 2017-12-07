# Ensure that the __init__ method gets documented
# (also see autoclass_content="both" setting),
INCLUDE_MEMBERS = {'__init__'}

# Members to hide.
EXCLUDE_MEMBERS = {
    # BaseForm
    'base_fields',
    'declared_fields',
    'Meta',

    # BaseModelAdmin
    'declared_fieldsets',
    'fieldsets',

    # Wagtail Page
    'panels',
    'content_panels',

    # Polymorphic
    'polymorphic_primary_key_name',
    'polymorphic_super_sub_accessors_replaced',
}
