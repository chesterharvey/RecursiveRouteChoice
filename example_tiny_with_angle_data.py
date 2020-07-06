# TODO check np.dot usage since numpy is not aware of sparse properly, should use A.dot(v)
import time
import numpy as np
from main import RecursiveLogitModel, RecursiveLogitDataStruct


import os
import optimisers as op
from optimisers import OptimType

np.seterr(all='raise')  # all='print')
np.set_printoptions(precision=4, suppress=True)
np.set_printoptions(edgeitems=3)
np.core.arrayprint._line_width = 100
import warnings
warnings.simplefilter("error")

time_io_start = time.time()
# file ="ExampleTutorial"# "ExampleTutorial" from classical logicv2
# file = "ExampleTiny"  # "ExampleNested" from classical logit v2, even smaller network
subfolder = "ExampleTiny"  # big data from classical v2
folder = os.path.join("Datasets", subfolder)

# Get observations matrix - note: observation matrix is in sparse format, but is of the form
#   each row == [dest node, orig node, node 2, node 3, ... dest node, 0 padding ....]
network_data_struct, obs_mat = RecursiveLogitDataStruct.from_directory(folder, add_angles=True,
                                                                       angle_type='comparison')
for i in network_data_struct.data_array:
    print(i.toarray())
# time_io_end = time.time()
#
# optimiser = op.LineSearchOptimiser(op.OptimHessianType.BFGS,
#                                    vec_length=1,
#                                    max_iter=4)  # TODO check these parameters & defaults
# print(type(obs_mat))
# model = RecursiveLogitModel(network_data_struct, optimiser, user_obs_mat=obs_mat)
#
#
# log_like_out, grad_out = model.get_log_likelihood()
#
# model.hessian = np.identity(network_data_struct.n_dims)
# n = 0
# print("Initial Values:")
# optimiser.set_beta_vec(model.beta_vec)
# optimiser.set_current_value(log_like_out)
# print(optimiser._line_search_iteration_log(model))
# while n <= 1000:
#     optimiser.iter_count += 1
#     if model.optimiser.METHOD_FLAG == OptimType.LINE_SEARCH:
#         ok_flag, hessian, log_msg = optimiser.line_search_iteration(model, verbose=False)
#         if ok_flag:
#             print(log_msg)
#         else:
#             raise ValueError("Line search error flag was raised. Process failed.")
#     else:
#         raise NotImplementedError("Only have line search implemented")
#
#     # check stopping condition
#     is_stopping, stop_type, is_successful = optimiser.check_stopping_criteria()
#
#     if is_stopping:
#         print(f"The algorithm stopped due to condition: {stop_type}")
#         break
#
# if n == 1000:
#     print("Infinite loop happened somehow, shouldn't have happened")
#
# time_finish = time.time()
# # tODO covariance
# print(f"IO time - {round(time_io_end - time_io_start, 3)}s")
# print(f"Algorithm time - {round(time_finish - time_io_end, 3)}")
#
# print(incidence_mat.toarray())