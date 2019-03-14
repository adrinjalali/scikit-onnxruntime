# Licensed under the MIT License.

# -*- coding: UTF-8 -*-
import unittest
import os
import sys
import numpy as np
import pandas
from sklearn.pipeline import make_pipeline
from sklearn.decomposition import PCA
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
import onnxruntime
from onnxruntime.capi._pybind_state import onnxruntime_ostream_redirect
from onnxruntime.datasets import get_example
from skl2onnx.common.data_types import FloatTensorType
from skl2onnx import convert_sklearn
from skonnxrt.sklapi import OnnxTransformer


class TestInferenceSessionSklearn(unittest.TestCase):

    def get_name(self, name):
        return get_example(name)

    def test_transform_numpy(self):
        x = np.array([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]], dtype=np.float32)
        name = self.get_name("mul_1.pb")
        with open(name, "rb") as f:
            content = f.read()

        tr = OnnxTransformer(content)
        tr.fit()
        res = tr.transform(x)
        exp = np.array([[1., 4.], [9., 16.], [25., 36.]], dtype=np.float32)
        self.assertEqual(list(res.ravel()), list(exp.ravel()))

    def test_transform_list(self):
        x = [[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]]
        name = self.get_name("mul_1.pb")
        with open(name, "rb") as f:
            content = f.read()

        tr = OnnxTransformer(content)
        tr.fit()
        res = tr.transform(x)
        exp = np.array([[1., 4.], [9., 16.], [25., 36.]], dtype=np.float32)
        self.assertEqual(list(res.ravel()), list(exp.ravel()))

    def test_transform_dict(self):
        x = {'X': np.array([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]])}
        name = self.get_name("mul_1.pb")
        with open(name, "rb") as f:
            content = f.read()

        tr = OnnxTransformer(content)
        tr.fit()
        res = tr.transform(x)
        exp = np.array([[1., 4.], [9., 16.], [25., 36.]], dtype=np.float32)
        self.assertEqual(list(res.ravel()), list(exp.ravel()))

    def test_transform_dataframe(self):
        x = pandas.DataFrame(data=[[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]])
        x.columns = "X1 X2".split()
        name = self.get_name("mul_1.pb")
        with open(name, "rb") as f:
            content = f.read()

        tr = OnnxTransformer(content)
        tr.fit()
        try:
            tr.transform(x)
        except RuntimeError:
            pass

    def test_multiple_transform(self):
        x = pandas.DataFrame(data=[[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]])
        x.columns = "X1 X2".split()
        name = self.get_name("mul_1.pb")
        with open(name, "rb") as f:
            content = f.read()

        res = list(OnnxTransformer.enumerate_create(content))
        assert len(res) > 0
        for k, tr in res:
            tr.fit()
            try:
                tr.transform(x)
            except RuntimeError:
                pass

    def test_pipeline_iris(self):
        iris = load_iris()
        X, y = iris.data, iris.target
        pipe = make_pipeline(PCA(n_components=2), LogisticRegression())
        pipe.fit(X, y)
        onx = convert_sklearn(pipe, initial_types=[
                              ('input', FloatTensorType((1, X.shape[1])))])
        onx_bytes = onx.SerializeToString()
        res = list(OnnxTransformer.enumerate_create(onx_bytes))
        outputs = []
        shapes = []
        for k, tr in res:
            outputs.append(k)
            tr.fit()
            y = tr.transform(X)
            self.assertEqual(y.shape[0], X.shape[0])
            shapes.append(y.shape)
        self.assertEqual(len(set(outputs)), len(outputs))
        shapes = set(shapes)
        self.assertEqual(shapes, {(150, 3), (150, 4), (150, 2), (150,)})


if __name__ == '__main__':
    unittest.main()
