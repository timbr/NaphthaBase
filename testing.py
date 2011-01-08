import unittest
import populatedb
import decimal

#////////////////////////////////////////////////////////////////////////////#
class TestDataContainer(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)
        self.container = populatedb.DataContainer()

    def testaddentry(self):
        self.container.addentry('testentry')
        self.assertEqual(self.container._dataline, ['testentry'])
        self.container.addentry(decimal.Decimal('5.54'))
        self.assertEqual(self.container._dataline, ['testentry', '5.54'], 'Needs to convert Decimal types to strings')
    
    def testaddline(self):
        self.container.addentry('mouse')
        self.container.addentry(decimal.Decimal('3.14'))
        self.assertEqual(self.container._dataline, ['mouse', '3.14'])
        self.assertEqual(self.container.datatable, [])
        self.container.addline()
        self.assertEqual(self.container._dataline, [])
        self.assertEqual(self.container.datatable, [['mouse', '3.14']])
        self.container.addentry('dog')
        self.container.addentry(decimal.Decimal('1.234'))
        self.container.addline()
        self.assertEqual(self.container.datatable, [['mouse', '3.14'], ['dog', '1.234']])
        self.assertEqual(self.container._dataline, [])

    def testprocess(self):
        datablock = ((1, 'random', '3.45', 'sausage'),
                     (2, 'doughnut', '5.46', 'burger'),
                     (3, 'carrot', '8.74', 'hailstorm'))
        self.container.process(datablock)
        self.assertEqual(self.container.datatable, 
                    [[1, 'random', '3.45', 'sausage'],
                     [2, 'doughnut', '5.46', 'burger'],
                     [3, 'carrot', '8.74', 'hailstorm']])

    def testcombine(self):
        self.assertEqual(self.container.combine('24 Acascia Avenue,', 'Stretford,', 'Manchester'), '24 Acascia Avenue\nStretford\nManchester')
        self.assertEqual(self.container.combine('monkey:', 'rat:', 'toad:', filter = ':', separator = '\t'), 'monkey\trat\ttoad')
        self.assertEqual(self.container.combine('pie\n', 'peas\n', 'ale\n', filter = '\n', separator = '--'), 'pie--peas--ale')
        

#////////////////////////////////////////////////////////////////////////////#
class TestQuickReference(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)
        self.reftable = populatedb.QuickReference()

    def testcreate_memory_table(self):
        fields = ('id', 'code', 'description')
        self.reftable.create_memory_table(table = 'material', fields = fields)
        self.assertTrue(len(self.reftable.memorydata) > 1000)
        self.assertEqual(type(self.reftable.memorydata), list)
        entry = self.reftable.memorydata[54]
        self.assertEqual(entry.id, 55)
        self.assertEqual(entry.code, 'ABS31C')
        self.assertEqual(entry.description, 'NATURAL ABS REGRIND')
        
        self.reftable.create_memory_table(table = 'hauliers', fields = '')
        print len(self.reftable.memorydata)
        self.assertEqual(len(self.reftable.memorydata), 13)
        entry = self.reftable.memorydata[10]
        self.assertEqual(entry.__dict__, {'name': 'PALLEX', 'lastupdated': '2009-07-24 09:10:10', 'haulierkey': 'PALLEX', 'rr_recordno': 11, 'nominalcode': '7400', 'id': 11})

    def testgetid(self):
        self.reftable.create_memory_table(table = 'material', fields = '')
        self.assertEqual(self.reftable.get_id(code = 'ABS31C'), 55)
        self.assertEqual(self.reftable.get_id(reply = 'description', code = 'PA11'), 'NATURAL PA6')
        self.reftable.create_memory_table(table = 'salesitem', fields = '')
        self.assertEqual(self.reftable.get_id(won = '21546', material_id = 288), 9905)
        self.reftable.create_memory_table(table = 'purchaseitem', fields = '')
       # self.assertEqual(self.reftable.get_id(pon = '3162', material_id = 797), 9905)

        
        


if __name__ == '__main__':
    unittest.main()