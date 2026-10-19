import aclib

# A straight railing (the edge of a gallery) and an L-shaped one, created far outside
# the model. The railing is read back with GetDetailsOfElements and its 3D box: the
# reference line, base and height must be the ones given.

createdRailings = aclib.RunTapirCommand ('CreateRailings', {
    'railingsData': [
        {
            'referenceLinePoints': [
                { 'x': 90.0, 'y': 0.0 },
                { 'x': 90.0, 'y': 2.18 }
            ],
            'zCoordinate': 0.0,
            'height': 1.0
        },
        {
            'referenceLinePoints': [
                { 'x': 95.0, 'y': 0.0 },
                { 'x': 98.0, 'y': 0.0 },
                { 'x': 98.0, 'y': 2.0 }
            ],
            'zCoordinate': 0.0,
            'height': 1.1,
            'refLineLocation': 'Center'
        }
    ]
})['elements']

details = aclib.RunTapirCommand ('GetDetailsOfElements', {
    'elements': createdRailings
}, debug = False)['detailsOfElements']

for detail in details:
    railing = detail['details']
    print ('{} with {} points, base {:.3f}, height {:.3f}'.format (
        detail['type'], len (railing['referenceLinePoints']), railing['zCoordinate'], railing['height']))

boundingBoxes = aclib.RunTapirCommand ('Get3DBoundingBoxes', {
    'elements': createdRailings
}, debug = False)['boundingBoxes3D']
for boundingBox in boundingBoxes:
    box = boundingBox['boundingBox3D']
    print ('3D box height: {:.2f}'.format (box['zMax'] - box['zMin']))

aclib.RunTapirCommand ('DeleteElements', {
    'elements': createdRailings
})
