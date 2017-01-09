import unittest
import sys
import os

def test():
    """Runs the unit tests without coverage."""
    tests = unittest.TestLoader().discover('tests')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    else:
        return 1


if __name__ == '__main__':

    if len(sys.argv) > 1:

        if sys.argv[1] == 'set':

            # Set test environment
            if sys.argv[2] == 'test':
                os.environ['APP_SETTINGS'] = 'TESTING'
                print 'Alfred changed to <Test> mode'

            # Set development environment
            if sys.argv[2] == 'dev':
                os.environ['APP_SETTINGS'] = 'DEVELOPMENT'
                print 'Alfred changed to <Development> mode'

            print '$APP_SETTINGS = ', os.environ['APP_SETTINGS'], '\n'
    else:
        print "############################################################"
        print "#########        Starting Alfred test suite        #########"
        print "############################################################"
        test()
