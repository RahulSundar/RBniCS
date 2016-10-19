# Copyright (C) 2015-2016 by the RBniCS authors
#
# This file is part of RBniCS.
#
# RBniCS is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# RBniCS is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with RBniCS. If not, see <http://www.gnu.org/licenses/>.
#
## @file distribution.py
#  @brief Type for distribution
#
#  @author Luca      Venturi  <luca.venturi@sissa.it>
#  @author Davide    Torlo    <davide.torlo@sissa.it>
#  @author Francesco Ballarin <francesco.ballarin@sissa.it>
#  @author Gianluigi Rozza    <gianluigi.rozza@sissa.it>
#  @author Alberto   Sartori  <alberto.sartori@sissa.it>

from abc import ABCMeta, abstractmethod

class Distribution(object):
    __metaclass__ = ABCMeta
    
    ## Sample n points from the distribution
    @abstractmethod
    def sample(self, box, n):
        raise NotImplementedError("The method sample is distribution-specific and needs to be overridden.")
        
    ## Override the following methods to use a Distribution as a dict key
    def __hash__(self):
        dict_values_for_hash = self.__dict__.values()
        dict_for_hash = list()
        for v in dict_values_for_hash:
            if isinstance(v, dict):
                dict_for_hash.append( tuple(v.values()) )
            elif isinstance(v, list):
                dict_for_hash.append( tuple(v) )
            else:
                dict_for_hash.append(v)
        return hash((type(self).__name__, tuple(dict_for_hash)))
        
    def __eq__(self, other):
        return (type(self).__name__, self.__dict__) == (type(other).__name__, other.__dict__)
        
    def __ne__(self, other):
        return not(self == other)
        
