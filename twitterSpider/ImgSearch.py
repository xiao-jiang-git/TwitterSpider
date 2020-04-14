# -*- coding: utf-8 -*-

import turicreate as tc
import os


class Img_search():

    def model_generate(self):
        data = tc.image_analysis.load_images('/Users/jiang/Pictures/picture', with_path=True, recursive=True)# recursive 递归目录遍历


        data['name'] = data['path'].apply(lambda path: os.path.basename(os.path.dirname(path)))

        data.explore()

        model = tc.image_similarity.create(data)

        model.save('picture_model')

    def img_search(self):
        test_data = tc.image_analysis.load_images('/Users/jiang/Pictures/test', with_path=True, recursive=True)

        test_data.explore()

        loaded_model = tc.load_model('picture_model')

        similar_images = loaded_model.query(test_data, label='path', k=3)

        return similar_images
