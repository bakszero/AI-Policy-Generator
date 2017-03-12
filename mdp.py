#!/bin/env python
"""
9.15 Value Iteration 3
==============================

We got the following world::

    +--+-----+-----+-----+-----+
    |  |  1  |  2  |  3  |  4  |
    +--+-----+-----+-----+-----+
    |A |     |     |     | +100|
    +--+-----+-----+-----+-----+
    |B |     |#####|     | -100|
    +--+-----+-----+-----+-----+
    |C |     |     |     |     |
    +--+-----+-----+-----+-----+

The goal is in A4 with a reward of +100. B4 is a trap. B2 is blocked.

When heading into the target direction the target field is successfully
reached with a probability of 0.8. Adjacent fields (90 deg angle) with 0.1.

We should calculate the optimal policy.

Result::

    +--+---------------+----------------+----------------+---------------+
    |0 |          85.0 |           89.0 |           93.0 |            100|
    +--+---------------+----------------+----------------+---------------+
    |1 |          81.0 |           None |           68.0 |           -100|
    +--+---------------+----------------+----------------+---------------+
    |2 |          77.0 |           73.0 |           70.0 |           47.0|
    +--+---------------+----------------+----------------+---------------+

"""
__author__ = 'Jan Beilicke <dev +at+ jotbe-fx +dot+ de>'
__date__ = '2011-11-11'

__coauthor__ = 'Bakhtiyar Syed'
__date__ = '2017-03-11'
import sys, math


class ValueIterator:

    def __init__(self, world,  prev_world, read_only, delta, prob_target=1.0, prob_left=0.0, prob_right=0.0, \
                prob_back=0.0, state_reward=0.0, discount_factor=1.0 ):
        self.world = world
        self.prev_world = prev_world
        self.prob_target = prob_target
        self.prob_left = prob_left
        self.prob_right = prob_right
        self.prob_back = prob_back
        self.state_reward = state_reward
        self.read_only_states = read_only
        self.discount_factor = discount_factor
        self.delta = delta

    def iterate(self, iterations):
        for i in range(iterations):
            print ('\n')
            print ('\n')
            print('_' * 80)
            

            for row in range(len(self.world)):
                for col in range(len(self.world[row])):
                    if (row, col) in self.read_only_states:
                        continue
                    
                    print('Iteration %d' % int(i + 1))
                    print('Estimating S(%d,%d)' % (row, col))
                    self.world[row][col] = self.bellman_update((row, col))

                    self.print_world(decimal_places=4)
            
            #Before updating previous world to reflect the new world changes, we need to check for diff and if diff < delta
            #How do we do that? Trying to implement...
            list = []
            for row in range(len(self.world)):
                for col in range(len(self.world[row])):
                    if (row, col) in self.read_only_states:
                        continue

                    list.append((self.world[row][col] - self.prev_world[row][col])) 
            
            print "List for utility change: "
            print list
                    
            
            print "Change of utility's max = " + str(max(list))
            
            i = max(list)
            print i
            for j in range(len(list)):
                if (i == list[j]):
                    print "coords of max utility change is "
                    print j

            if (max(list) < self.delta):
                #print list
                return


            #Update previous world to the new world
            #print self.prev_world
            #print self.world

            for row in range(len(self.world)):
                for col in range(len(self.world[row])):
                    if (row, col) in self.read_only_states:
                        continue
                    self.prev_world[row][col] = self.world[row][col]
            

    def bellman_update(self, state_coords):
        r, c = state_coords

        e_coords = (r, c + 1)
        s_coords = (r + 1, c)
        w_coords = (r, c - 1)
        n_coords = (r - 1, c)

        e_util = self.get_utility_of_state(self.prev_world[r][c], e_coords)
        s_util = self.get_utility_of_state(self.prev_world[r][c], s_coords)
        w_util = self.get_utility_of_state(self.prev_world[r][c], w_coords)
        n_util = self.get_utility_of_state(self.prev_world[r][c], n_coords)

        print('own_value%s = %d' % ((r, c), self.world[r][c]))
        #print('e_util%s = %f' % (e_coords, e_util))
        #print('s_util%s = %f' % (s_coords, s_util))
       # print('w_util%s = %f' % (w_coords, w_util))
       # print('n_util%s = %f' % (n_coords, n_util))

        print 'E: '
        e_value = self.value_function(e_util, n_util, s_util, w_util)
        print('e_value%s = %f' % (e_coords, self.state_reward+ e_value))
        print  'S: '
        s_value = self.value_function(s_util, e_util, w_util, n_util) 
        print('s_value%s = %f' % (s_coords, self.state_reward+s_value))
        print 'W: '
        w_value = self.value_function(w_util, s_util, n_util, e_util)
        print('w_value%s = %f' % (w_coords, self.state_reward+w_value))
        print 'N: '
        n_value = self.value_function(n_util, w_util, e_util, s_util)
        print('n_value%s = %f' % (n_coords, self.state_reward+n_value))

        print ('\n')
        print 'MAX IS : ' + str(max(self.state_reward+e_value, self.state_reward+s_value, self.state_reward+w_value, self.state_reward+n_value))
        
        
        

        xx =  (self.state_reward) + self.discount_factor * max(e_value, s_value, w_value, n_value)
        print 'Total utility for this state: ' #+ (self.state_reward) + ' ' + '+' +' '+ (self.discount_factor)+ ' '+ '*'+ ' '+ 'max( '+e_value+' '+s_val
        print xx
        return xx
    def get_utility_of_state(self, own_value, target_coords):
        row, col = target_coords

        if row < 0 or col < 0:
            print('Bumping against a wall in S(%d,%d)' % (row, col))
            return own_value

        try:
            value = self.prev_world[row][col] or own_value
        except IndexError:
            print('Bumping against a wall in S(%d,%d)' % (row, col))
            value = own_value
        return float(value)

    def value_function(self, target, left=0, right=0, back=0):
        xy = float(self.prob_target * target + \
            self.prob_left * left + \
            self.prob_right * right +\
            self.prob_back * back)

        print "-0.85 + " +str(self.prob_target) + str("*(")+ str(target)+str(") + ") +str(self.prob_left) + str("*(")+str(left)+str(") + ")+str(self.prob_right) + str("*(")+str(right)+str(") ")
        return xy

    def print_world(self, decimal_places=0):
        for row in range(len(self.world)):
            print('-' * 70)
            sys.stdout.write(str(row))
            for col in range(len(self.world[row])):
                val = self.world[row][col]
                if type(val) == float:
                    val = round(val, decimal_places)
                sys.stdout.write(' | %14s' % val)
            print('|')
        print('-' * 70)


if __name__ == '__main__':

    world = [
                [None, None, 17, None],
                [0,   0,  0,   0],
                [0, -17, None, 0],
                [0, 0, 0, 0]
            ]
    prev_world = [
                [None, None, 17, None],
                [0,   0,  0,   0],
                [0, -17, None, 0],
                [0, 0, 0, 0]
            ]
    read_only_states = [(0, 0), (0, 1), (0, 2), (0,3), (2,1), (2,2)]

    # For stochastic actions
    Vi_stochastic = ValueIterator(world, prev_world,read_only_states, prob_target=0.8, prob_left=0.1, prob_right=0.1, state_reward=-0.85 , delta=0.85)
    
    Vi_stochastic.iterate(100)

    # For stochastic actions with no costs
    #Vi_stochastic = ValueIterator(world, read_only_states, prob_target=0.8, prob_left=0.1, prob_right=0.1, state_reward=0, discount_factor=0.1)
    #Vi_stochastic.iterate(100)

    # For deterministic actions
    #Vi_deterministic = ValueIterator(world, read_only_states, prob_target=1, state_reward=-3)
   # Vi_deterministic.iterate(50)

    # For stochastic actions with high costs (even higher then the ditch in (0,4))
    # "This is an extreme case. I don't know why it would make sense to set a penalty for life that is
    # so negative that even negative death is worse than living."
    #Vi_stochastic = ValueIterator(world, read_only_states, prob_target=0.8, prob_left=0.1, prob_right=0.1, state_reward=-200)
    #Vi_stochastic.iterate(50)