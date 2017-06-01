# Copyright (C) 2015-2017 by the RBniCS authors
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

from rbnics.utils.decorators import Extends, override, ReductionMethodDecoratorFor
from rbnics.eim.problems import DEIM, EIM, ExactParametrizedFunctions

@ReductionMethodDecoratorFor(ExactParametrizedFunctions, replaces=(DEIM, EIM))
def ExactParametrizedFunctionsDecoratedReductionMethod(DifferentialProblemReductionMethod_DerivedClass):
    
    @Extends(DifferentialProblemReductionMethod_DerivedClass, preserve_class_name=True)
    class ExactParametrizedFunctionsDecoratedReductionMethod_Class(DifferentialProblemReductionMethod_DerivedClass):
        @override
        def __init__(self, truth_problem, **kwargs):
            # Call the parent initialization
            DifferentialProblemReductionMethod_DerivedClass.__init__(self, truth_problem, **kwargs)
        
        @override
        def set_training_set(self, ntrain, enable_import=True, sampling=None, **kwargs):
            import_successful = DifferentialProblemReductionMethod_DerivedClass.set_training_set(self, ntrain, enable_import, sampling, **kwargs)
            # Since exact evaluation is required, we cannot use a distributed training set
            self.training_set.distributed_max = False
            return import_successful
        
        @override
        def _create_folders(self):
            # Precomputation of error estimation operators is disabled, so there is no need
            # to create the error estimation folder.
            error_estimation_folder = self.reduced_problem.folder.pop("error_estimation")
            # Call Parent
            output = DifferentialProblemReductionMethod_DerivedClass._create_folders(self)
            # Restore the "error_estimation" estimation key. We still need it in the dictionary
            # because it is an input argument to load/save methods of error estimation operators.
            # These methods, however, have been patched so that they don't save anything to disk.
            self.reduced_problem.folder["error_estimation"] = error_estimation_folder
            # Return
            return output
            
    # return value (a class) for the decorator
    return ExactParametrizedFunctionsDecoratedReductionMethod_Class
    
