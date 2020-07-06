
"""Very minimal correctness checks to make sure i don't accidentally break stuff. very black box,
more intended to detect errors rather than be specific about where they are

"""


import pytest

import numpy as np
from scipy import linalg
from scipy.sparse import csr_matrix

from data_loading import load_csv_to_sparse, get_incorrect_tien_turn_matrices, \
    get_uturn_categorical_matrix, get_left_turn_categorical_matrix
from main import RecursiveLogitModel, get_value_func_grad, RecursiveLogitDataSet

import os
from os.path import join
import optimisers as op


class TestSimpleCases:

    def test_first_example(self):
        subfolder = "ExampleTiny"  # big data from classical v2
        folder = join("../Datasets", subfolder)
        INCIDENCE = "incidence.txt"
        TRAVEL_TIME = 'travelTime.txt'
        OBSERVATIONS = "observations.txt"
        TURN_ANGLE = "turnAngle.txt"
        file_incidence = os.path.join(folder, INCIDENCE)
        file_travel_time = os.path.join(folder, TRAVEL_TIME)
        file_turn_angle = os.path.join(folder, TURN_ANGLE)
        file_obs = os.path.join(folder, OBSERVATIONS)
        row, col, data = np.loadtxt(file_travel_time, unpack=True)
        incidence_data = np.ones(len(data))  # TODO where do i need this?

        travel_times_mat = load_csv_to_sparse(file_travel_time).todok()
        incidence_mat = load_csv_to_sparse(file_incidence, dtype='int').todok()
        turn_angle_mat = load_csv_to_sparse(file_turn_angle).todok()

        # turn turn angle data into uturn and left turn dummies
        print(turn_angle_mat.toarray())

        left_turn_dummy = get_left_turn_categorical_matrix(turn_angle_mat)
        u_turn_dummy = get_uturn_categorical_matrix(turn_angle_mat)

        # Get observations matrix - note: observation matrix is in sparse format, but is of the form
        #   each row == [dest node, orig node, node 2, node 3, ... dest node, 0 padding ....]
        obs_mat = load_csv_to_sparse(file_obs, dtype='int', square_matrix=False).todok()

        network_data_struct = RecursiveLogitDataSet(travel_times=travel_times_mat,
                                                    incidence_matrix=incidence_mat,
                                                    turn_angles=None)
        optimiser = op.LineSearchOptimiser(op.OptimType.LINE_SEARCH, op.OptimHessianType.BFGS,
                                           vec_length=1,
                                           max_iter=4)  # TODO check these parameters & defaults

        model = RecursiveLogitModel(network_data_struct, optimiser, user_obs_mat=obs_mat)

        beta = np.array(-1.5)  # default value, 1d for now
        data = network_data_struct

        log_like_out, grad_out = model.get_log_likelihood()
        eps = 1e-6
        assert np.abs(log_like_out - 0.6931471805599454) < eps
        assert np.abs(linalg.norm(grad_out) - 0) < eps

        model.hessian = np.identity(data.n_dims)
        out_flag, hessian, log = optimiser.line_search_iteration(model,verbose=False)
        assert out_flag == True
        assert (hessian == np.identity(2)).all()
        assert optimiser.n_func_evals == 1

    def test_turn_angle_matrices(self):
        """ Note the problem of generating these kind of matrices is ignored"""
        a = np.array([[0, -0.1, 180, ],
                      [90, 0, -90],
                      [-45, -15, 0]])

        b = a * np.pi / 180
        b = csr_matrix(b)
        actual_left_turn = get_left_turn_categorical_matrix(b.todok()).toarray()
        actual_u_turn = get_uturn_categorical_matrix(b.todok()).toarray()

        expected_left_turn = np.array([[0, 0, 0], [0, 0, 1], [1, 0, 0]])
        expected_u_turn = np.array([[0, 0, 1], [0, 0, 0], [0, 0, 0]])
        assert (expected_left_turn == actual_left_turn).all()
        assert (expected_u_turn == actual_u_turn).all()