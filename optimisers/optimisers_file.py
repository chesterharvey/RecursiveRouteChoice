import functools
from enum import Enum, auto

import numpy as np

from .hessian_approx import update_hessian_approx, OptimHessianType
from .line_search import line_search_asrch




class OptimType(Enum):
    LINE_SEARCH = auto()
    TRUST_REGION = auto()


class Optimiser(object):
    """Global wrapper object around all optim algs, delegate to sub classes for individual.
    Need to be clear about which properties are effectively read only and which store state.
    Ideally this is a generic optim alg that doesn't know anything about RecursiveLogitModel
    TODO currently is intrinsically dependent"""
    def __init__(self, method=OptimType.LINE_SEARCH, hessian_type=OptimHessianType.BFGS,
                 vec_length=1,
                 max_iter = 4):
        self.method = method
        self.hessian_type = hessian_type
        self.n = vec_length
        self.max_iter = max_iter

        self.n_func_evals = 0
        self.tol = 1e-6


class LineSearchOptimiser(Optimiser):
    INITIAL_STEP_LENGTH = 1.0
    NEGATIVE_CURVATURE_PARAMETER = 0.0
    SUFFICIENT_DECREASE_PARAMETER = 0.0001
    CURVATURE_CONDITION_PARAMETER = 0.9
    X_TOLERANCE = 2.2e-16
    MINIMUM_STEP_LENGTH = 0
    MAXIMUM_STEP_LENGTH = 1000

    def __init__(self, method=OptimType.LINE_SEARCH, hessian_type=OptimHessianType.BFGS,
                 vec_length=1, max_iter=4, ):
        super().__init__(method, hessian_type, vec_length, max_iter)
        #TODO adjust fields?


    def line_search_iteration(self, model):
        """ TODO note there is som first time initialisation that need to be removed"""
        hessian_old = model.hessian
        value, grad = model.get_log_likelihood()

        p = np.linalg.solve(hessian_old, -grad)

        if np.dot(p, grad) > 0:
            p = -p

        def line_arc(step, ds):
            return (step * ds, ds)  # TODO note odd function form

        arc = functools.partial(line_arc, ds=p)
        stp = self.INITIAL_STEP_LENGTH
        x = model.get_beta_vec()
        optim_func = model.get_log_like_new_beta

        OPTIMIZE_CONSTANT_MAX_FEV = 10 #TODO sort out how function evals are tracked
        x, val_new, grad_new, stp, info, n_func_evals = line_search_asrch(
            optim_func, x, value, grad, arc, stp,
            maxfev=OPTIMIZE_CONSTANT_MAX_FEV)

        if val_new <= value:
            # TODO need to collect these things into a struct
            #   think there already is an outline of one
            step = p * stp
            delta_grad = grad_new - grad
            value = val_new
            x = x
            grad = grad_new
            hessian, ok = update_hessian_approx(model, step, delta_grad, hessian_old)  # TODO write
            # this
            print(hessian)
            out_flag = True
        else:
            out_flag = False
            hessian = hessian_old

        return out_flag, hessian



class TrustRegionOptimiser(Optimiser):

    def __init__(self, method=OptimType.LINE_SEARCH, hessian_type=OptimHessianType.BFGS,
                 vec_length=1, max_iter = 4, ):
        super().__init__(method, hessian_type, vec_length, max_iter)
        raise NotImplementedError()











