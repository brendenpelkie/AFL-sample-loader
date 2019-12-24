#!python
from __future__ import division,print_function
from NistoRoboto.Mixture import Mixture
from NistoRoboto.Component import Component
import unittest
import numpy as np

class Mixture_TestCase(unittest.TestCase):
    def test_create(self):
        '''Can we create a Mixture object? '''
        density1 = 1.11
        volume1 = 0.5
        mass1 = volume1*density1
        D2O = Component('D2O',density=density1,volume=volume1,mass=mass1)

        density2 = 1.00
        volume2 = 0.15
        mass2 = volume2*density2
        H2O = Component('H2O',density=density2,volume=volume2,mass=mass2)

        mix = Mixture([H2O,D2O])

        new_density = (D2O.mass + H2O.mass)/(D2O.mass/D2O.density + H2O.mass/H2O.density)
        np.testing.assert_almost_equal(mix.mass,D2O.mass+H2O.mass)
        np.testing.assert_almost_equal(mix.volume,D2O.volume+H2O.volume)
        np.testing.assert_almost_equal(mix.density,new_density)

    def test_add(self):
        '''Can we add more of a component to a Mixture object? '''
        density1 = 1.11
        volume1 = 0.5
        mass1 = volume1*density1
        D2O_1 = Component('D2O',density=density1,volume=volume1,mass=mass1)
        D2O_2 = (D2O_1*1.35)

        density2 = 1.00
        volume2 = 0.15
        mass2 = volume2*density2
        H2O = Component('H2O',density=density2,volume=volume2,mass=mass2)

        mix = (Mixture([H2O,D2O_1]) + D2O_2)


        new_density = (D2O_1.mass + D2O_2.mass + H2O.mass)/(D2O_1.mass/D2O_1.density + D2O_2.mass/D2O_2.density + H2O.mass/H2O.density)
        np.testing.assert_almost_equal(mix.mass  ,D2O_1.mass  +D2O_2.mass  +H2O.mass)
        np.testing.assert_almost_equal(mix.volume,D2O_1.volume+D2O_2.volume+H2O.volume)
        np.testing.assert_almost_equal(mix.density,new_density)

        # ensure the D2O component was properly combined
        np.testing.assert_array_almost_equal(mix['D2O'].mass  ,D2O_1.mass  +D2O_2.mass)
        np.testing.assert_array_almost_equal(mix['D2O'].volume,D2O_1.volume+D2O_2.volume)

    def test_add_new(self):
        '''Can we add a new component to a Mixture object? '''
        # create three components
        density1 = 1.11
        volume1 = 0.5
        mass1 = volume1*density1
        D2O = Component('D2O',density=density1,volume=volume1,mass=mass1)

        density2 = 1.00
        volume2 = 0.15
        mass2 = volume2*density2
        H2O = Component('H2O',density=density2,volume=volume2,mass=mass2)

        density3 = 0.789
        mass3 =  0.3
        EtOH = Component('EtOH',formula='C2H5OH',density=density3,mass=mass3)

        # create base mixture then add third component
        solution = Mixture([H2O,D2O]) 
        mix = solution + EtOH

        # base sanity check
        self.assertTrue(mix.contains('D2O'))
        self.assertTrue(mix.contains('H2O'))
        self.assertTrue(mix.contains('EtOH'))


        # ensure total solution properties 
        new_density = (D2O.mass + H2O.mass + EtOH.mass)/(D2O.mass/D2O.density + H2O.mass/H2O.density + EtOH.mass/EtOH.density)
        np.testing.assert_almost_equal(mix.mass  ,D2O.mass  + H2O.mass  + EtOH.mass)
        np.testing.assert_almost_equal(mix.volume,D2O.volume + H2O.volume+EtOH.volume)
        np.testing.assert_almost_equal(mix.density,new_density)

    def test_set_volume_fraction(self):
        '''Can we set the volume fraction of the mixture?'''
        density1 = 1.11
        volume1 = 0.5
        mass1 = volume1*density1
        D2O = Component('D2O',density=density1,volume=volume1,mass=mass1)

        density2 = 1.00
        volume2 = 0.15
        mass2 = volume2*density2
        H2O = Component('H2O',density=density2,volume=volume2,mass=mass2)

        density3 = 0.789
        mass3 =  0.3
        volume3 = mass3/density3
        EtOH = Component('EtOH',formula='C2H5OH',density=density3,mass=mass3,volume=volume3)


        mix = Mixture([D2O,H2O,EtOH])

        np.testing.assert_almost_equal(mix.volume_fraction['D2O'],volume1/(volume1+volume2+volume3))
        np.testing.assert_almost_equal(mix.volume_fraction['H2O'],volume2/(volume1+volume2+volume3))
        np.testing.assert_almost_equal(mix.volume_fraction['EtOH'],volume3/(volume1+volume2+volume3))
        vfrac_set = {'D2O':0.1,'H2O':0.5,'EtOH':0.4}
        mix.set_volume_fractions(vfrac_set)

        #sanity check
        np.testing.assert_almost_equal(mix.volume_fraction['D2O'],mix.volume_fraction['D2O'])
        np.testing.assert_almost_equal(mix.volume_fraction['H2O'],mix.volume_fraction['H2O'])
        np.testing.assert_almost_equal(mix.volume_fraction['EtOH'],mix.volume_fraction['EtOH'])

        np.testing.assert_almost_equal(mix['D2O'].volume,mix.volume*vfrac_set['D2O'])
        np.testing.assert_almost_equal(mix['H2O'].volume,mix.volume*vfrac_set['H2O'])
        np.testing.assert_almost_equal(mix['EtOH'].volume,mix.volume*vfrac_set['EtOH'])

    def test_set_mass_fraction(self):
        '''Can we set the mass fraction of the mixture?'''
        density1 = 1.11
        volume1 = 0.5
        mass1 = volume1*density1
        D2O = Component('D2O',density=density1,volume=volume1,mass=mass1)

        density2 = 1.00
        volume2 = 0.15
        mass2 = volume2*density2
        H2O = Component('H2O',density=density2,volume=volume2,mass=mass2)

        density3 = 0.789
        mass3 =  0.3
        volume3 = mass3/density3
        EtOH = Component('EtOH',formula='C2H5OH',density=density3,mass=mass3,volume=volume3)

        mix = Mixture([D2O,H2O,EtOH])

        np.testing.assert_almost_equal(mix.mass_fraction['D2O'],mass1/(mass1+mass2+mass3))
        np.testing.assert_almost_equal(mix.mass_fraction['H2O'],mass2/(mass1+mass2+mass3))
        np.testing.assert_almost_equal(mix.mass_fraction['EtOH'],mass3/(mass1+mass2+mass3))
        
        mfrac_set = {'D2O':7/15,'H2O':8/30,'EtOH':4/15}
        mix.set_mass_fractions(mfrac_set)

        #sanity check
        np.testing.assert_almost_equal(mix.mass_fraction['D2O'],mix.mass_fraction['D2O'])
        np.testing.assert_almost_equal(mix.mass_fraction['H2O'],mix.mass_fraction['H2O'])
        np.testing.assert_almost_equal(mix.mass_fraction['EtOH'],mix.mass_fraction['EtOH'])

        np.testing.assert_almost_equal(mix['D2O'].mass,mix.mass*mfrac_set['D2O'])
        np.testing.assert_almost_equal(mix['H2O'].mass,mix.mass*mfrac_set['H2O'])
        np.testing.assert_almost_equal(mix['EtOH'].mass,mix.mass*mfrac_set['EtOH'])

    # def test_set_concentration(self):
    #     '''Can we set the concentration of a solute?'''
    #     density1 = 1.11
    #     volume1 = 0.5
    #     mass1 = volume1*density1
    #     D2O = Component('D2O',density=density1,volume=volume1,mass=mass1)

    #     density2 = 1.00
    #     volume2 = 0.15
    #     mass2 = volume2*density2
    #     H2O = Component('H2O',density=density2,volume=volume2,mass=mass2)


    #     # in order for this to work, we specifically don't set a density
    #     mass3 =  0.3
    #     volume3 = 0
    #     polymer = Component('poly',mass=mass3,volume=volume3)

    #     mix = Mixture([D2O,H2O,EtOH])
        
        
if __name__ == '__main__':
    import unittest 
    suite = unittest.TestLoader().loadTestsFromTestCase(Mixture_TestCase)
    unittest.TextTestRunner(verbosity=2).run(suite)
