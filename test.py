import pandas as pd


satu1 = pd.read_excel('Экспорт из сату satu export-products .xlsx')
satuIds1 = satu1['Код_товара'].tolist()
satuNames1 = satu1['Название_позиции'].tolist()
satuPhotos1 = satu1['Ссылка_изображения'].tolist()
satuLinks1 = satu1['Продукт_на_сайте'].tolist()
satuUnique1 = satu1['Идентификатор_товара'].tolist()
dictPhotos = {}
dictTDPhotos = {}
for n in range(len(satu1)):
    description_1 = '''
<div>
  <div class="custom-set b-similar-products">
   <span class="b-title">
    Комплект
   </span>
   <ul class="b-similar-products__list">
    <li class="b-similar-products__item">
     <a class="b-similar-products__image-link" company_sites-similar_company_products="" href="LINK_ID" onclick="require('Metrics').ga.track_event('similar_products'," target="_self" title="">
      <img class="b-similar-products__image" src="PHOTO_ID" style="height: 400px; weight: 400px;"/>
     </a>
     <div class="b-similar-products__title">
      <a class="b-similar-products__link" company_sites-similar_company_products="" href="LINK_ID" onclick="require('Metrics').ga.track_event('similar_products'," target="_self">
      </a>
      <span class="b-similar-products__hider">
            Артикул: SATU_ID
      </span>
     </div>
    </li>
   </ul>
  </div>
  <script>
   document.addEventListener('DOMContentLoaded', function() { setTimeout("$('.custom-set').insertAfter('div.b-product__social-links:first'", 2000); });
  </script>
 </div>
'''
    description_1 = description_1.replace('LINK_ID', str(satuLinks1[n]))
    description_1 = description_1.replace('NAME_ID', str(satuNames1[n]))
    description_1 = description_1.replace('SATU_ID', str(satuIds1[n]))
    description_1 = description_1.replace('PHOTO_ID', str(satuPhotos1[n]).split(',')[0])
    dictPhotos[str(satuIds1[n])] = description_1
    dictTDPhotos[str(satuUnique1[n])] = description_1
