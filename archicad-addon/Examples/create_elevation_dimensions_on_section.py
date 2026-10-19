import aclib

# Level markers on the slabs of the first section of the Project Map: one elevation
# dimension per slab with the top and bottom face heights, measured from the project
# zero and shown with a plus sign (+2.78). The section window must be the active one,
# as for every dimension created on section elements.
navigatorTree = aclib.RunCommand ('API.GetNavigatorItemTree', {
    'navigatorTreeId': { 'type': 'ProjectMap' }
})

def FindSections (item, foundItems):
    for child in item.get ('children', []):
        navigatorItem = child['navigatorItem']
        if navigatorItem.get ('type') == 'SectionItem':
            foundItems.append (navigatorItem['navigatorItemId'])
        FindSections (navigatorItem, foundItems)
    return foundItems

sectionNavigatorItemIds = FindSections (navigatorTree['navigatorTree']['rootItem'], [])
if not sectionNavigatorItemIds:
    print ('No section found in the Project Map.')
else:
    databases = aclib.RunTapirCommand ('GetDatabaseIdFromNavigatorItemId', {
        'navigatorItemIds': [
            { 'navigatorItemId': sectionNavigatorItemIds[0] }
        ]
    })['databases']

    sectionElements = aclib.RunTapirCommand ('GetSectionElements', {
        'databases': databases
    })['sectionElements']
    slabSectionElements = [
        s for s in sectionElements if s.get ('ownerElementType') == 'Slab'
    ]

    created = aclib.RunTapirCommand ('CreateAssociativeDimensionsOnSection', {
        'dimensionsData': [
            {
                'sectionElementId': s['sectionElementId'],
                'referencePoint': { 'x': -1.0, 'y': 0.0 },
                'preset': 'SlabSkinBorders',
                'skinBorderIndices': [0],
                'appearance': 'Elevation',
                'elevationOrigin': 'ProjectZero',
                'needPlus': True
            } for s in slabSectionElements
        ]
    })['elements']

    createdIds = [e for e in created if 'elementId' in e]
    if createdIds:
        details = aclib.RunTapirCommand ('GetDetailsOfElements', {
            'elements': createdIds
        }, debug = False)['detailsOfElements']
        for detail in details:
            dimension = detail['details']
            print ('{} with {} level markers'.format (dimension['appearance'], len (dimension['witnessPoints'])))
        aclib.RunTapirCommand ('DeleteElements', {
            'elements': createdIds
        })
