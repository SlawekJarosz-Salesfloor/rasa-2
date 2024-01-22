
# Model health report
## Index
 - [Overview](#overview)
 - [Config](#configs)
 - [Intents](#intents)
 - [Entities](#entities)
 - [NLU](#nlu)
 - [Core](#core)
 - [E2E Coverage](#e2e)


## Overview <a name='overview'></a>

### Bot info
|Bot Name|Creation date|Updated date|
|:-:|:-:|:-:|
|<span style='font-size:16px'>My project</span>|<span style='font-size:16px'>20/01/24 21:01:44</span>|<span style='font-size:16px'>21/01/24 21:17:05</span>|


### Score
|Intent|Entity|NLU|Core|E2E Coverage|<span style='font-size:20px'>Overall</span>|
|:-:|:-:|:-:|:-:|:-:|:-:|
|10            |-            |9.32            |10            |2.50            |<span style='font-size:20px'>**3.46**</span>|
🟢            |❌            |🟢            |🟢            |🔴            |<span style='font-size:20px'>🔴</span>|
### Element count
Describe the number of elements in the chatbot.

|Element type|Total|
|:-:|:-:|
|Intents|3|
|Entities|291|
|Actions and Utters|1|
|Stories|3|
|Rules|2|



## Configs <a name='configs'></a>
Settings that were used in the training *pipeline* and *policies*.
```yaml
# The config recipe.
# https://rasa.com/docs/rasa/model-configuration/
recipe: default.v1

# The assistant project unique identifier
# This default value must be replaced with a unique assistant name within your deployment
assistant_id: 20240121-200240-easy-buffet

# Configuration for Rasa NLU.
# https://rasa.com/docs/rasa/nlu/components/
language: en

pipeline: null
# # No configuration for the NLU pipeline was provided. The following default pipeline was used to train your model.
# # If you'd like to customize it, uncomment and adjust the pipeline.
# # See https://rasa.com/docs/rasa/tuning-your-model for more information.
#   - name: WhitespaceTokenizer
#   - name: RegexFeaturizer
#   - name: LexicalSyntacticFeaturizer
#   - name: CountVectorsFeaturizer
#   - name: CountVectorsFeaturizer
#     analyzer: char_wb
#     min_ngram: 1
#     max_ngram: 4
#   - name: DIETClassifier
#     epochs: 100
#     constrain_similarities: true
#   - name: EntitySynonymMapper
#   - name: ResponseSelector
#     epochs: 100
#     constrain_similarities: true
#   - name: FallbackClassifier
#     threshold: 0.3
#     ambiguity_threshold: 0.1

# Configuration for Rasa Core.
# https://rasa.com/docs/rasa/core/policies/
policies: null
# # No configuration for policies was provided. The following default policies were used to train your model.
# # If you'd like to customize them, uncomment and adjust the policies.
# # See https://rasa.com/docs/rasa/policies for more information.
#   - name: MemoizationPolicy
#   - name: RulePolicy
#   - name: UnexpecTEDIntentPolicy
#     max_history: 5
#     epochs: 100
#   - name: TEDPolicy
#     max_history: 5
#     epochs: 100
#     constrain_similarities: true

```

## Intents <a name='intents'></a>
Section that discusses metrics on model intents.

### Metrics
Table with the metrics of intentions.
|#||intent|Precision|Recall|F1 Score|Examples|
|:-:|-|-|-|-|-|-|
|1|🟢|goodbye|100.0%|100.0%|100.0%|10|
|2|🟢|mood_great|100.0%|100.0%|100.0%|14|
|3|🟢|greet|100.0%|100.0%|100.0%|13|
|4|🟢|mood_unhappy|100.0%|100.0%|100.0%|14|
|5|🟢|affirm|100.0%|100.0%|100.0%|6|
|6|🟢|bot_challenge|100.0%|100.0%|100.0%|4|
|7|🟢|deny|100.0%|100.0%|100.0%|7|

### Confused intentions
Where all the confusing or wrong sentences of the model are listed.

No confusions or errors of intent were found in this model.
### Histogram
![Histogram](results/intent_histogram.png 'Histogram')
### Confusion Matrix
![Confusion Matrix](results/intent_confusion_matrix.png 'Confusion Matrix')

## Entities <a name='entities'></a>
Section that discusses metrics about the model entities.

### Metrics
Table with entity metrics.


No entities were found in this model.

### Confused entities
Where all the confusing or wrong entities of the model are listed.

No confusions of entities were found in this model.

## NLU <a name='nlu'></a>
Section that discusses metrics about NLU and its example phrases.

### Sentences
Table with metrics for bot training phrases.

|#||Text|Intent|Predicted intent|Confidence|Understood|
|:-:|-|-|-|-|-|-|
|1|🟢|Iconic Princess [Raincoat]{"entity": "sf_apparel_product_type__raincoat"}|sf_apparel__title_tags|sf_apparel__title_tags|100.0%|✅|
|2|🟢|Aidan Sherpa [Windbreaker]{"entity": "sf_apparel_product_type__windbreaker"}|sf_apparel__title_tags|sf_apparel__title_tags|100.0%|✅|
|3|🟢|Chris [Low Rise]{"entity": "sf_apparel_rise__low_rise"} Jeans|sf_apparel__title_tags|sf_apparel__title_tags|100.0%|✅|
|4|🟢|[Lightweight]{"entity": "sf_apparel_material_weight__lightweight"} Ponte Topper|sf_apparel__title_tags|sf_apparel__title_tags|100.0%|✅|
|5|🟢|[Heavyweight]{"entity": "sf_apparel_material_weight__heavyweight"} [Fleece]{"entity": "sf_apparel_material__fleece"} Pullover|sf_apparel__title_tags|sf_apparel__title_tags|100.0%|✅|
|6|🟢|[Midweight]{"entity": "sf_apparel_material_weight__midweight"} Knit [Jacket]{"entity": "sf_apparel_product_type__jacket"}|sf_apparel__title_tags|sf_apparel__title_tags|100.0%|✅|
|7|🟢|Crafted of [satin]{"entity": "sf_apparel_material__satin"}; this [halterneck]{"entity": "sf_apparel_neckline__halter"} [gown]{"entity": "sf_apparel_product_type__gown"} from Mac Duggal features a flared silhouette. This sleeveless style is finished with [ruched]{"entity": "sf_apparel_product_type__ruched"} detailing and an open back. [Halterneck]{"entity": "sf_apparel_neckline__halter"}. [Sleeveless]{"entity": "sf_apparel_sleeve_length__sleeveless"}. [Back zip closure]{"entity": "sf_apparel_closure__zipper__back_zipper"}. [Lined]{"entity": "sf_apparel_lining__lined"}. 100% [polyester]{"entity": "sf_apparel_material__polyester"}. Spot clean. Imported.|sf_apparel__description_tags|sf_apparel__description_tags|100.0%|✅|
|8|🟢|Featuring a voluminous flared skirt; Mac Duggal's midi dress is decorated with gleaming [sequin]{"entity": "sf_apparel_embellishments__sequins"} embellishments. [Roundneck]{"entity": "sf_apparel_neckline__roundneck"}. [Long sleeves]{"entity": "sf_apparel_sleeve_length__long_sleeves"}. [Center back zipper]{"entity": "sf_apparel_closure__zipper__back_zipper"}. 100% [polyester]{"entity": "sf_apparel_material__polyester"}. [Lining]{"entity": "sf_apparel_lining__lined"}: polyester. Spot clean. Imported.|sf_apparel__description_tags|sf_apparel__description_tags|100.0%|✅|
|9|🟢|Alexander Wang's bi color [crop]{"entity": "sf_apparel_length__cropped"} hoodie is crafted of cotton knit. This pullover style flaunts [long sleeves]{"entity": "sf_apparel_sleeve_length__long_sleeves"}; a spacious [kangaroo pocket]{"entity": "sf_apparel_pocket_type__kangaroo"}; and a glittered puff logo at the front. Hood. Long sleeves. Kangaroo front pocket. Pulls over. 100% [cotton]{"entity": "sf_apparel_material__cotton"}. Trim: 99% cotton; 1% [elastane]{"entity": "sf_apparel_material__elastane"}. [Dry clean only]{"entity": "sf_apparel_care_instructions__dry_clean_only"}. Made in Portugal.|sf_apparel__description_tags|sf_apparel__description_tags|100.0%|✅|
|10|🟢|Cut in a [cropped silhouette]{"entity": "sf_apparel_length__cropped"}; ASTR The Label's woven Madrigal jacket is elevated by [puff sleeves]{"entity": "sf_apparel_sleeve_style__puff"} and a [crystal button front]{"entity": "sf_apparel_closure__button"}. Plunging V neck. [Long puff sleeves]{"entity": "sf_apparel_sleeve_length__long_sleeves"}. [Crystal button front]{"entity": "sf_apparel_closure__button"}. Mock waist slip pockets. Fringe trim. [Lining]{"entity": "sf_apparel_lining__lined"}: 100% [polyester]{"entity": "sf_apparel_material__polyester"}. 40% [polyester]{"entity": "sf_apparel_material__polyester"} / 30% [wool]{"entity": "sf_apparel_material__wool"} / 30% [acrylic]{"entity": "sf_apparel_material__acrylic"}. [Dry clean]{"entity": "sf_apparel_care_instructions__dry_clean_only"}. Imported.|sf_apparel__description_tags|sf_apparel__description_tags|100.0%|✅|
|11|🟢| Quilted texture adds classic element to vest. [Stand collar]{"entity": "sf_apparel_collar__stand"}. [Sleeveless]{"entity": "sf_apparel_sleeve_length__sleeveless"}. [Zip front]{"entity": "sf_apparel_closure__zipper"} with [snap button closure]{"entity": "sf_apparel_closure__snap"}. [Waist snap button flap pockets]{"entity": "sf_apparel_pocket_type__flap_pockets"}. About 29.  5' from shoulder to hem. Shell / lining: Polyamide. [Machine wash]{"entity": "sf_apparel_care_instructions__machine_wash"}. Imported. Model shown is 5'10' (177cm) wearing US size 4.|sf_apparel__description_tags|sf_apparel__description_tags|100.0%|✅|
|12|🟢|Flaunting puffed shoulders and a flattering [V neck]{"entity": "sf_apparel_neckline__v_neck"}; Mac Duggal's elegant dress is adorned with three dimensional [floral appliqués]{"entity": "sf_apparel_embellishments__appliquéd"} with [sparking beads]{"entity": "sf_apparel_embellishments__beaded"}. This piece is finished with a [back leg slit]{"entity": "sf_apparel_slit__back_slit"}. [V neck]{"entity": "sf_apparel_neckline__v_neck"}. [Long sleeves]{"entity": "sf_apparel_sleeve_length__long_sleeves"}. [Center back zipper]{"entity": "sf_apparel_closure__zipper__back_zipper"}. 100% [polyester]{"entity": "sf_apparel_material__polyester"}. Lining: 100% [polyester]{"entity": "sf_apparel_material__polyester"}. Spot clean. Imported.|sf_apparel__description_tags|sf_apparel__description_tags|100.0%|✅|
|13|🟢|A.  L.  C.  's Davin jacket boasts an elongated; tailored silhouette and classic [notch lapels]{"entity": "sf_apparel_collar__lapel__notch"}. Goldtone buttons and bracelet length [long sleeves]{"entity": "sf_apparel_sleeve_length__long_sleeves"} complete the look. Notch lapels. Long sleeves; [buttoned cuffs]{"entity": "sf_apparel_cuff__buttoned"}. [Chest welt pocket]{"entity": "sf_apparel_pocket_type__chest_pocket"}. [Side flap pockets]{"entity": "sf_apparel_pocket_type__flap_pockets"}. Interior pocket. [Button front closure]{"entity": "sf_apparel_closure__button"}. 68% polyester / 29% viscose / 3% elastane. Lining: 51% polyester / 49% cotton. Sleeve lining: 100% [polyester]{"entity": "sf_apparel_material__polyester"}. [Dry clean]{"entity": "sf_apparel_care_instructions__dry_clean_only"}. Imported of Portuguese fabric.|sf_apparel__description_tags|sf_apparel__description_tags|100.0%|✅|
|14|🟢|Crafted of Italian wool; this [oversized]{"entity": "sf_apparel_fit__oversized"} Bottega Veneta coat boasts a tailored double breasted design. This design features [notch lapels]{"entity": "sf_apparel_collar__lapel__notch"} and [patch pockets]{"entity": "sf_apparel_pocket_type__patch_pockets"}. [Notch lapels]{"entity": "sf_apparel_collar__lapel__notch"}. [Long sleeves]{"entity": "sf_apparel_sleeve_length__long_sleeves"}. [Front button closure]{"entity": "sf_apparel_closure__button"}. [Front patch pockets]{"entity": "sf_apparel_pocket_type__patch_pockets"}. 98% [wool]{"entity": "sf_apparel_material__wool"} / 1% [elastane]{"entity": "sf_apparel_material__elastane"} / 1% polyamide. [Lining]{"entity": "sf_apparel_lining__lined"}: 100% viscose. 100% [polyester]{"entity": "sf_apparel_material__polyester"} fill. Combo: 100% [cotton]{"entity": "sf_apparel_material__cotton"}. [Dry clean]{"entity": "sf_apparel_care_instructions__dry_clean_only"}. Made in Italy.|sf_apparel__description_tags|sf_apparel__description_tags|100.0%|✅|
|15|🟢|Decorated with mixed painterly [floral]{"entity": "sf_apparel_pattern__floral"} prints; Veronica Beard's [sleeveless]{"entity": "sf_apparel_sleeve_length__sleeveless"} Florencia maxi dress offers a crisscross bodice and tiered skirt. [Crisscross halterneck]{"entity": "sf_apparel_neckline__halter"}. [Sleeveless]{"entity": "sf_apparel_sleeve_length__sleeveless"}. Banded waist. [Thigh high front slit]{"entity": "sf_apparel_slit__front_slit"}. [Concealed side zip closure]{"entity": "sf_apparel_closure__zipper__side_zipper"}. Keyhole back cut out; [button closures]{"entity": "sf_apparel_closure__button"}. 100% [silk]{"entity": "sf_apparel_material__silk"}. [Dry clean]{"entity": "sf_apparel_care_instructions__dry_clean_only"}. Imported.|sf_apparel__description_tags|sf_apparel__description_tags|100.0%|✅|
|16|🟢|Veronica Beard's fitted Brompton dress is crafted of [jersey]{"entity": "sf_apparel_material__jersey"}. This [ruched]{"entity": "sf_apparel_product_type__ruched"} style features a [round neck]{"entity": "sf_apparel_neckline__roundneck"}; padded shoulders; and an asymmetric hem. [Round neck]{"entity": "sf_apparel_neckline__roundneck"}. [Sleeveless]{"entity": "sf_apparel_sleeve_length__sleeveless"}. Pulls over. 95% [modal]{"entity": "sf_apparel_material__modal"}; 5% [spandex]{"entity": "sf_apparel_material__elastane"}. [Machine wash]{"entity": "sf_apparel_care_instructions__machine_wash"}. Imported.|sf_apparel__description_tags|sf_apparel__description_tags|100.0%|✅|
|17|🟢|From the Apparis x Mansur Gavriel Collection. Apparis' Milly coat is composed of plant based PLUCHE™ faux fur and features wide notch lapels. Wide notch lapels. [Long sleeves]{"entity": "sf_apparel_sleeve_length__long_sleeves"}. [Side welt pockets]{"entity": "sf_apparel_pocket_type__welt_pockets"}. Hook and eye closure. Fur type: PLUCHE faux fur. Faux fur: 67% [polyester]{"entity": "sf_apparel_material__polyester"} / 33% other fibers. [Lining]{"entity": "sf_apparel_lining__lined"}: 100% polyester. [Dry clean]{"entity": "sf_apparel_care_instructions__dry_clean_only"}. Imported.|sf_apparel__description_tags|sf_apparel__description_tags|100.0%|✅|
|18|🟢|Complete with a removable [buckle]{"entity": "sf_apparel_waist__belt"} [belt]{"entity": "sf_apparel_waist__belt"}; RUDSAK's Audrey down puffer jacket is elevated by a [detachable zip hood]{"entity": "sf_apparel_hood_type__detachable"} and a [contrast faux fur]{"entity": "sf_apparel_material__faux_fur"} trim. Detachable zip hood. Dropped shoulders. [Long sleeves]{"entity": "sf_apparel_sleeve_length__long_sleeves"}. [Removable buckle belt]{"entity": "sf_apparel_waist__belt"}. [Mock waist flap pockets]{"entity": "sf_apparel_pocket_type__flap_pockets"}; [snap closures]{"entity": "sf_apparel_closure__snap"}. [Zip front closure]{"entity": "sf_apparel_closure__zipper"}. 100% [nylon]{"entity": "sf_apparel_material__nylon"}. Lining: 100% [nylon]{"entity": "sf_apparel_material__nylon"}. Down: 90 / 10 duck down. Filling: 800+ fill power. Trim: 82% nylon / 18% elastane. Fur type: Faux. [Machine wash]{"entity": "sf_apparel_care_instructions__machine_wash"}. Imported.|sf_apparel__description_tags|sf_apparel__description_tags|100.0%|✅|
|19|🟢|Sachin & Babi's Camila midi dress features a fitted silhouette crafted of [ruched]{"entity": "sf_apparel_product_type__ruched"} stretch crepe. An O ring waistband and an [asymmetric flared]{"entity": "sf_apparel_product_type__asymmetrical"} hem complete the look. [Round neck]{"entity": "sf_apparel_neckline__roundneck"}. [Sleeveless]{"entity": "sf_apparel_sleeve_length__sleeveless"}. O ring waistband. [Back hook and eye closure]{"entity": "sf_apparel_closure__hook_and_eye"}. [Concealed side zip closure]{"entity": "sf_apparel_closure__zipper__side_zipper"}. 100% [polyester]{"entity": "sf_apparel_material__polyester"}. [Lined]{"entity": "sf_apparel_lining__lined"}. [Dry clean]{"entity": "sf_apparel_care_instructions__dry_clean_only"}. Imported.|sf_apparel__description_tags|sf_apparel__description_tags|100.0%|✅|
|20|🟢|Trina Turk's Global caftan dress flaunts a colorful print on luxe [silk]{"entity": "sf_apparel_material__silk"}. [Boatneck]{"entity": "sf_apparel_neckline__roundneck__boat_neck"}. [Dolman sleeves]{"entity": "sf_apparel_sleeve_style__dolman"}. Pullover style. 100% [silk]{"entity": "sf_apparel_material__silk"}. [Dry clean]{"entity": "sf_apparel_care_instructions__dry_clean_only"}. Imported.|sf_apparel__description_tags|sf_apparel__description_tags|100.0%|✅|
|21|🟢|This Carolina [midi dress]{"entity": "sf_apparel_length__midi"} from Trina Turk features a skirt crafted from layers of circular [chiffon]{"entity": "sf_apparel_material__chiffon"} [appliques]{"entity": "sf_apparel_embellishments__appliquéd"}. It's finished with a [V neck]{"entity": "sf_apparel_neckline__v_neck"} and [adjustable spaghetti straps]{"entity": "sf_apparel_straps__adjustable"}. V neck. Adjustable spaghetti straps. Circular applique hem.  [Side zip]{"entity": "sf_apparel_closure__zipper__side_zipper"}100% [polyesterDry]{"entity": "sf_apparel_material__polyester"} cleanImported|sf_apparel__description_tags|sf_apparel__description_tags|100.0%|✅|
|22|🟢|The Levi's 80's [Mom]{"entity": "sf_apparel_product_type__mom"} Jeans feature a relaxed fit through the hip and thigh. This style is finished with [distressing]{"entity": "sf_apparel_distressing__distressed"} at the knee and a [tapered leg]{"entity": "sf_apparel_product_type__tapered"}. Five pocket style. [Zip fly]{"entity": "sf_apparel_closure__zipper"}. Tapered leg. 100% [cotton]{"entity": "sf_apparel_material__cotton"}. [Machine wash]{"entity": "sf_apparel_care_instructions__machine_wash"}. Imported.|sf_apparel__description_tags|sf_apparel__description_tags|100.0%|✅|
|23|🟢|UGG's Patricia puffer jacket is lined in the label's signature plush sherpa for outstanding warmth and comfort. This piece is styled with an oversized envelope collar and logo patch on the sleeve. Oversized collar. [Long sleeves]{"entity": "sf_apparel_sleeve_length__long_sleeves"}. Knit storm cuffs. [Front snap closures]{"entity": "sf_apparel_closure__snap"}. [Welt pockets]{"entity": "sf_apparel_pocket_type__welt_pockets"} with soft fleece hand warmer pocket linings. 100% [polyester]{"entity": "sf_apparel_material__polyester"} (water resistant). [Lining]{"entity": "sf_apparel_lining__lined"}: [Synthetic down fill]{"entity": "sf_apparel_material_composition__synthetic"} ([polyester]{"entity": "sf_apparel_material__polyester"}). Trim: 100% [polyester]{"entity": "sf_apparel_material__polyester"} sherpa. [Dry clean]{"entity": "sf_apparel_care_instructions__dry_clean_only"}. Imported.|sf_apparel__description_tags|sf_apparel__description_tags|100.0%|✅|
|24|🟢|Trina Turk's short sleeve Enchantress dress offers a wrap bodice and draped detailing at the skirt. Shawl collar. [V neck]{"entity": "sf_apparel_neckline__v_neck"}. Short [raglan]{"entity": "sf_apparel_sleeve_style__raglan"} sleeves. [Elasticized]{"entity": "sf_apparel_waist__elastic"} waist. Pulls over. 100% [polyester]{"entity": "sf_apparel_material__polyester"}. [Dry clean]{"entity": "sf_apparel_care_instructions__dry_clean_only"}. Imported.|sf_apparel__description_tags|sf_apparel__description_tags|100.0%|✅|
|25|🟢|A beautiful floral design adds texture to this classic knit jacket from Ming Wang. [Modified mandarin collar]{"entity": "sf_apparel_collar__mandarin"}. [Long sleeves]{"entity": "sf_apparel_sleeve_length__long_sleeves"}. [Single button closure]{"entity": "sf_apparel_closure__button"}. 50% [acrylic]{"entity": "sf_apparel_material__acrylic"} / 45% [rayon]{"entity": "sf_apparel_material__rayon"} / 5% [polyester]{"entity": "sf_apparel_material__polyester"}. [Machine wash]{"entity": "sf_apparel_care_instructions__machine_wash"}. Imported.|sf_apparel__description_tags|sf_apparel__description_tags|100.0%|✅|
|26|🟢|Veronica Beard's tiered Lexington [maxi]{"entity": "sf_apparel_length__maxi"} dress features mixed painterly [floral]{"entity": "sf_apparel_pattern__floral"} prints and a tonal self tie belt for convertible styling. Plunging [V neck]{"entity": "sf_apparel_neckline__v_neck"}. [Cap sleeves]{"entity": "sf_apparel_sleeve_style__cap"}; [rolled cuffs]{"entity": "sf_apparel_cuff__rolled"}. [Self tie belt]{"entity": "sf_apparel_waist__belt"}. [Button front]{"entity": "sf_apparel_closure__button"}. 100% [cotton]{"entity": "sf_apparel_material__cotton"}. [Dry clean]{"entity": "sf_apparel_care_instructions__dry_clean_only"}. Imported.|sf_apparel__description_tags|sf_apparel__description_tags|100.0%|✅|
|27|🟢|Apparais' Dasha coat is cut from [faux shearling]{"entity": "sf_apparel_material__faux_fur"}. This double breasted piece is designed with a [mid length]{"entity": "sf_apparel_length__mid_length"}. Wide notch lapels. [Long sleeves]{"entity": "sf_apparel_sleeve_length__long_sleeves"}. [Side welt pockets]{"entity": "sf_apparel_pocket_type__welt_pockets"}. [Double breasted button closure]{"entity": "sf_apparel_closure__button"}. [Fur type: faux]{"entity": "sf_apparel_material__faux_fur"} shearling. Faux shearling: 80% [polyester]{"entity": "sf_apparel_material__polyester"} / 20% hemp. [Lining]{"entity": "sf_apparel_lining__lined"}: 100% polyester. [Dry clean]{"entity": "sf_apparel_care_instructions__dry_clean_only"}. Imported.|sf_apparel__description_tags|sf_apparel__description_tags|100.0%|✅|
|28|🟢|we have a variety of elegant styles and [sleeve]{"entity": "sf_apparel_NO_MATCH__sleeves"} lengths that would be perfect for your occasion.|sf_apparel__description_tags|sf_apparel__description_tags|100.0%|✅|
|29|🟢|For a classy date night look, I recommend a chic and elegant A Line dress in a sophisticated and timeless color like black or navy. Consider a midi or knee-length dress for a refined and polished appearance. Opt for a dress with a flattering neckline such as a sweetheart or V-neck to add a touch of allure. Look for subtle embellishments like lace or a tasteful slit for a touch of sophistication. Lastly, choose a dress with a slim or fit and flare silhouette for a graceful and refined ensemble.|sf_apparel__description_tags|sf_apparel__description_tags|100.0%|✅|
|30|🟢|Complete the ensemble with a pair of strappy sandals and delicate accessories to complement the cheerful and celebratory atmosphere of the wedding.|sf_apparel__NO_MATCH|sf_apparel__NO_MATCH|100.0%|✅|
|31|🟢|[Rhinestone]{"entity": "sf_apparel_embellishments__rhinestone"} Column Dress|sf_apparel__title_tags|sf_apparel__title_tags|100.0%|✅|
|32|🟢|Canyon Jeweled [Faux Leather]{"entity": "sf_apparel_material__faux_leather"} [Jacket]{"entity": "sf_apparel_product_type__jacket"}|sf_apparel__title_tags|sf_apparel__title_tags|100.0%|✅|
|33|🟢|Adriana [Handkerchief Hem]{"entity": "sf_apparel_hem__handkerchief"} Dress|sf_apparel__title_tags|sf_apparel__title_tags|100.0%|✅|
|34|🟢|The Donovan jacket from A.  L.  C. is made of [plaid]{"entity": "sf_apparel_pattern__plaid"} [patterned linen]{"entity": "sf_apparel_material__linen"} [blend]{"entity": "sf_apparel_material_composition__blend"} in a [longline silhouette]{"entity": "sf_apparel_length__long"}.  [Peak lapels]{"entity": "sf_apparel_collar__lapel__peak"}. Padded shoulders. [Long sleeves]{"entity": "sf_apparel_sleeve_length__long_sleeves"}. [Waist flap pockets]{"entity": "sf_apparel_pocket_type__flap_pockets"}. [Front button closure]{"entity": "sf_apparel_closure__button"}. 60% [linen]{"entity": "sf_apparel_material__linen"} / 37% [viscose]{"entity": "sf_apparel_material__viscose"} / 3% [elastane]{"entity": "sf_apparel_material__elastane"}. Lining: 51% [polyester]{"entity": "sf_apparel_material__polyester"} / 49% [cotton]{"entity": "sf_apparel_material__cotton"}. [Dry clean]{"entity": "sf_apparel_care_instructions__dry_clean_only"}. Imported.|sf_apparel__description_tags|sf_apparel__description_tags|100.0%|✅|
|35|🟢|Mac Duggal's beaded and [sequined]{"entity": "sf_apparel_embellishments__sequins"} gown boasts a lustrous checkered pattern. Cut in an [A line]{"entity": "sf_apparel_fit__a_line"} silhouette; this style is complete with a pleated asymmetric skirt. [Plunging V neckline]{"entity": "sf_apparel_neckline__v_neck"}. [Long sleeves]{"entity": "sf_apparel_sleeve_length__long_sleeves"}. [Concealed back zip]{"entity": "sf_apparel_closure__zipper__back_zipper"}. [Asymmetric hem]{"entity": "sf_apparel_product_type__asymmetrical"}. [Lining]{"entity": "sf_apparel_lining__lined"}: 100% [polyester]{"entity": "sf_apparel_material__polyester"}. 100% [polyester]{"entity": "sf_apparel_material__polyester"}. [Spot clean]{"entity": "sf_apparel_care_instructions__hand_wash"}. Imported.|sf_apparel__description_tags|sf_apparel__description_tags|100.0%|✅|
|36|🟢|From the [denim innovators of 7]{"entity": "sf_apparel_material__denim"} For All Mankind. Every pair of JEN7 jeans features the enhanceME sculpting panel; built right into the pockets and engineered to subtly slim and sculpt your curves. [Belt loops]{"entity": "sf_apparel_waist__belt__belt_loops"}. [Five pocket style]{"entity": "sf_apparel_pocket_type__pocket"}. [Zip fly]{"entity": "sf_apparel_closure__zipper"}. [Cotton]{"entity": "sf_apparel_material__cotton"} / [polyester]{"entity": "sf_apparel_material__polyester"} / rayon / [spandex]{"entity": "sf_apparel_material__elastane"}. [Machine wash]{"entity": "sf_apparel_care_instructions__machine_wash"}. Imported.|sf_apparel__description_tags|sf_apparel__description_tags|100.0%|✅|
|37|🟢|From the Ieena Collection. A layered tulle skirt lends whimsy to Mac Duggal’s [sequined]{"entity": "sf_apparel_embellishments__sequins"} bustier gown. [Sweetheart neckline]{"entity": "sf_apparel_neckline__sweetheart"}. [Self tie spaghetti straps]{"entity": "sf_apparel_straps__spaghetti"}. [Concealed back zip]{"entity": "sf_apparel_closure__zipper__back_zipper"}. Banded waist. Tiered tulle skirt. [Polyester]{"entity": "sf_apparel_material__polyester"}. [Dry clean]{"entity": "sf_apparel_care_instructions__dry_clean_only"}. Imported.|sf_apparel__description_tags|sf_apparel__description_tags|100.0%|✅|
|38|🟢|Xirena's Eloise Dress is crafted of an airy cotton blend to an easy [midi]{"entity": "sf_apparel_length__midi"} length with gathered shaping along the empire waist. [V neck]{"entity": "sf_apparel_neckline__v_neck"}. [Long sleeves]{"entity": "sf_apparel_sleeve_length__long_sleeves"} with banded cuffs. Pullover style. [Ruched bust]{"entity": "sf_apparel_product_type__ruched"}. [Empire waist]{"entity": "sf_apparel_waist__empire"}. [On seam pockets]{"entity": "sf_apparel_pocket_type__pocket"}. [Cotton]{"entity": "sf_apparel_material__cotton"} / [rayon]{"entity": "sf_apparel_material__rayon"}. [Machine wash]{"entity": "sf_apparel_care_instructions__machine_wash"}. Made in USA.|sf_apparel__description_tags|sf_apparel__description_tags|100.0%|✅|
|39|🟢|Woven from a luxe [linen blend]{"entity": "sf_apparel_material_composition__blend"}; this asymmetric [maxi]{"entity": "sf_apparel_length__maxi"} dress is defined by adjustable self tie gathering at shoulder and side. [Boatneck]{"entity": "sf_apparel_neckline__roundneck__boat_neck"}. [Adjustable self tie cap sleeve]{"entity": "sf_apparel_sleeve_style__cap"}. [Adjustable self tie side]{"entity": "sf_apparel_closure__side_tie"}. [Side seam pockets]{"entity": "sf_apparel_pocket_type__pocket"}. [Asymmetric hem]{"entity": "sf_apparel_product_type__asymmetrical"}. Pullover style. 58% [linen]{"entity": "sf_apparel_material__linen"} / 39% [viscose]{"entity": "sf_apparel_material__viscose"} / 3% polyurethane. [Dry clean]{"entity": "sf_apparel_care_instructions__dry_clean_only"}. Made in USA.|sf_apparel__description_tags|sf_apparel__description_tags|100.0%|✅|
|40|🟢|Crafted of [floral]{"entity": "sf_apparel_pattern__floral"} [lace]{"entity": "sf_apparel_material__lace"}; Sachin & Babi's Mon Coeur minidress is designed with a [flared silhouette]{"entity": "sf_apparel_fit__fit_and_flare"}. This [sleeveless]{"entity": "sf_apparel_sleeve_length__sleeveless"} style features a [heart cut out]{"entity": "sf_apparel_product_type__cutout"} [trimmed with beads]{"entity": "sf_apparel_embellishments__beaded"} at the back. [Round neck]{"entity": "sf_apparel_neckline__roundneck"}. [Sleeveless]{"entity": "sf_apparel_sleeve_length__sleeveless"}. [Back heart cut out]{"entity": "sf_apparel_product_type__cutout"}. [Back hook and bar closure]{"entity": "sf_apparel_closure__hook_and_bar"}. 100% [polyester]{"entity": "sf_apparel_material__polyester"}. [Dry clean]{"entity": "sf_apparel_care_instructions__dry_clean_only"}. Imported.|sf_apparel__description_tags|sf_apparel__description_tags|100.0%|✅|
|41|🟢|Michael Kors Collection’s Jamison slipdress features a curve skimming bodice that falls to a flared [maxi]{"entity": "sf_apparel_length__maxi"} skirt. This '90s inspired style is embellished with a crinkled finish. [Scoopneck]{"entity": "sf_apparel_neckline__roundneck__scoop_neck"}. [Spaghetti straps]{"entity": "sf_apparel_straps__spaghetti"}. [Concealed back zip closure]{"entity": "sf_apparel_closure__zipper__back_zipper"}. Crinkled finish. 71% [acetate]{"entity": "sf_apparel_material__acetate"} / 29% [viscose]{"entity": "sf_apparel_material__viscose"}. [Lining]{"entity": "sf_apparel_lining__lined"}: 100% [silk]{"entity": "sf_apparel_material__silk"}. [Dry clean]{"entity": "sf_apparel_care_instructions__dry_clean_only"}. Imported.|sf_apparel__description_tags|sf_apparel__description_tags|100.0%|✅|
|42|🟢|Free People's Jealousy jacket is crafted of luxurious worn in leather and features a semi fitted silhouette. [Notch lapels]{"entity": "sf_apparel_collar__lapel__notch"} and zip accents complete the look. Notch lapels. [Long sleeves]{"entity": "sf_apparel_sleeve_length__long_sleeves"}; zip cuffs. Chest and [side zip pockets]{"entity": "sf_apparel_pocket_type__zip_pockets"}. [Asymmetric zip closure]{"entity": "sf_apparel_closure__zipper"}. 100% cow [leather]{"entity": "sf_apparel_material__leather"}. [Dry clean]{"entity": "sf_apparel_care_instructions__dry_clean_only"}. Made in UK.|sf_apparel__description_tags|sf_apparel__description_tags|100.0%|✅|
|43|🟢|From lace adorned slip dresses to sculpted leather pieces and minimalist knits; Khaite's collection reimagines eveningwear; taking notes from '80s and '90s glamour. Creative Director Catherine Holstein juxtaposes structured separates with pleated and sheer paneled dresses and skirts. A hand painted lip print lends an element of whimsy to this array; redefining sensual elegance with an irreverently New York attitude. Oversize [studs]{"entity": "sf_apparel_embellishments__studs"} along the hem punctuate this Khaite Grizzo [denim]{"entity": "sf_apparel_material__cotton"} [jacket]{"entity": "sf_apparel_product_type__jacket"} replete with flat felled seams; [chest pockets]{"entity": "sf_apparel_pocket_type__chest_pocket"} and silvertone hardware. Spread collar. [Long sleeves]{"entity": "sf_apparel_sleeve_length__long_sleeves"}; [button cuffs]{"entity": "sf_apparel_cuff__buttoned"}. [Front button placket]{"entity": "sf_apparel_closure__button"}. 100% [cotton]{"entity": "sf_apparel_material_composition__natural"}. [Machine wash]{"entity": "sf_apparel_care_instructions__machine_wash"}. Imported.|sf_apparel__description_tags|sf_apparel__description_tags|100.0%|✅|
|44|🟢|Bridget is a [high rise]{"entity": "sf_apparel_rise__high_rise"}; cropped [boot cut]{"entity": "sf_apparel_product_type__bootcut"} fit [that utilizes our In]{"entity": "sf_apparel_wash__dark"}stasculpt technology to smooth; sculpt; and conform to your body for the perfect fit. Henderson is a [no fade black wash]{"entity": "sf_apparel_wash__dark"} with a [raw hem]{"entity": "sf_apparel_hem__raw"}. Fabric Detail: 91% [Cotton]{"entity": "sf_apparel_material__cotton"}; 7.5% [Polyester]{"entity": "sf_apparel_material__polyester"}; 1.5% [Lycra]{"entity": "sf_apparel_material__elastane"}. [5 pocket detail]{"entity": "sf_apparel_pocket_type__no_pockets"}. Contouring Waistband. [Machine wash cold]{"entity": "sf_apparel_care_instructions__machine_wash__cold_water"}; hang to dry.|sf_apparel__description_tags|sf_apparel__description_tags|100.0%|✅|
|45|🟢|Cut in a [cropped silhouette]{"entity": "sf_apparel_length__cropped"}; rag & bone's terry [crewneck]{"entity": "sf_apparel_neckline__roundneck__crewneck"} sweatshirt offers a relaxed fit and [banded ribbed trim]{"entity": "sf_apparel_hem__ribbed"}. [Crewneck]{"entity": "sf_apparel_neckline__roundneck__crewneck"}. Dropped shoulders. [Long sleeves]{"entity": "sf_apparel_sleeve_length__long_sleeves"}. [Banded ribbed trim]{"entity": "sf_apparel_hem__ribbed"}. Pullover style. 100% [cotton]{"entity": "sf_apparel_material__cotton"}. [Machine wash]{"entity": "sf_apparel_care_instructions__machine_wash"}. Imported.|sf_apparel__description_tags|sf_apparel__description_tags|100.0%|✅|
|46|🟢|This essential Apres Ski [jacket]{"entity": "sf_apparel_product_type__jacket"} features a high low hem and detachable Toscana [Lamb]{"entity": "sf_apparel_material__fur"} trim. Detachable Toscana [Lamb]{"entity": "sf_apparel_material__fur"} collar. Down filled sleeves with windbreaker cuffs. [Front zipper]{"entity": "sf_apparel_closure__zipper__front_zipper"}. Side [pockets]{"entity": "sf_apparel_pocket_type__pocket"} with snap closure. Filled with 80% white duck down and 20% white goose feathers. Fur Type: Toscana [Lamb]{"entity": "sf_apparel_material__fur"} trim; Dyed. Fur Origin: Spain. Professional cleaning only. Made in Italy.|sf_apparel__description_tags|sf_apparel__description_tags|100.0%|✅|
|47|🟢|do you any dresses?. sporty i guess with [sleeves]{"entity": "sf_apparel_NO_MATCH__sleeves"}|sf_apparel__description_tags|sf_apparel__description_tags|100.0%|✅|
|48|🟢|Shall we focus on a specific silhouette or detail that interests you?|sf_apparel__NO_MATCH|sf_apparel__NO_MATCH|100.0%|✅|
|49|🟢|Veronica Beard's Nayari dress is crafted of [cotton]{"entity": "sf_apparel_material__cotton"} and features a beautiful [ditsy floral print]{"entity": "sf_apparel_pattern__floral"}. [Geometric]{"entity": "sf_apparel_pattern__geometric"} [lace]{"entity": "sf_apparel_material__lace"} paneling throughout and a [split neck]{"entity": "sf_apparel_neckline__split_neck"} complete this [mini length piece]{"entity": "sf_apparel_length__mini"}. [Split neck]{"entity": "sf_apparel_neckline__split_neck"}. [Long sleeves]{"entity": "sf_apparel_sleeve_length__long_sleeves"}. [Button front closure]{"entity": "sf_apparel_closure__button"}. 100% [cotton]{"entity": "sf_apparel_material__cotton"}. [Dry clean]{"entity": "sf_apparel_care_instructions__dry_clean_only"}. Imported.|sf_apparel__description_tags|sf_apparel__description_tags|100.0%|✅|
|50|🟢|Enjoy your new dress at the party!|sf_apparel__NO_MATCH|sf_apparel__NO_MATCH|100.0%|✅|
|51|🟢|Iridescent [Fit & Flare]{"entity": "sf_apparel_fit__fit_and_flare"} Dress|sf_apparel__title_tags|sf_apparel__title_tags|100.0%|✅|
|52|🟢|Monroe [Leather]{"entity": "sf_apparel_material__leather"} Moto [Jacket]{"entity": "sf_apparel_product_type__jacket"}|sf_apparel__title_tags|sf_apparel__title_tags|100.0%|✅|
|53|🟢|Le Garcon Tailored [Boyfriend]{"entity": "sf_apparel_product_type__boyfriend"} Jeans|sf_apparel__title_tags|sf_apparel__title_tags|100.0%|✅|
|54|🟢|Shan [Tweed]{"entity": "sf_apparel_material__tweed"} & Chain Link [Jacket]{"entity": "sf_apparel_product_type__jacket"}|sf_apparel__title_tags|sf_apparel__title_tags|100.0%|✅|
|55|🟢|[Petite]{"entity": "sf_apparel_size_category__petite"} Quilted Eclipse Knit [Jacket]{"entity": "sf_apparel_product_type__jacket"}|sf_apparel__title_tags|sf_apparel__title_tags|100.0%|✅|
|56|🟢|Play [Ruffled]{"entity": "sf_apparel_hem__ruffled"} [Linen]{"entity": "sf_apparel_material__linen"} Dress|sf_apparel__title_tags|sf_apparel__title_tags|100.0%|✅|
|57|🟢|[Plus Size]{"entity": "sf_apparel_size_category__plus_size"} Embellished Cape [Velvet]{"entity": "sf_apparel_material__velvet"} [Gown]{"entity": "sf_apparel_product_type__gown"}|sf_apparel__title_tags|sf_apparel__title_tags|100.0%|✅|
|58|🟢|Knit [Zigzag]{"entity": "sf_apparel_pattern__geometric"} Fringe [Jacket]{"entity": "sf_apparel_product_type__jacket"}|sf_apparel__title_tags|sf_apparel__title_tags|100.0%|✅|
|59|🟢|[Metallic]{"entity": "sf_apparel_pattern__metallic"} Column [Gown]{"entity": "sf_apparel_product_type__gown"}|sf_apparel__title_tags|sf_apparel__title_tags|100.0%|✅|
|60|🟢|Lutece Dickey Double Breasted [Twill]{"entity": "sf_apparel_material__twill"} [Jacket]{"entity": "sf_apparel_product_type__jacket"}|sf_apparel__title_tags|sf_apparel__title_tags|100.0%|✅|
|61|🟢|[Bleach]{"entity": "sf_apparel_distressing__bleached"} [Straight Fit]{"entity": "sf_apparel_product_type__straight"} Jeans|sf_apparel__title_tags|sf_apparel__title_tags|100.0%|✅|
|62|🟢|Brandy [Graphic]{"entity": "sf_apparel_pattern__graphic"} [Sweatshirt]{"entity": "sf_apparel_product_type__sweatshirt"}|sf_apparel__title_tags|sf_apparel__title_tags|100.0%|✅|
|63|🟢|[Satin]{"entity": "sf_apparel_material__satin"} [Strapless]{"entity": "sf_apparel_straps__strapless"} Ballgown|sf_apparel__title_tags|sf_apparel__title_tags|100.0%|✅|
|64|🟢|Julia [Bow]{"entity": "sf_apparel_closure__bow"} Column [Gown]{"entity": "sf_apparel_product_type__gown"}|sf_apparel__title_tags|sf_apparel__title_tags|100.0%|✅|
|65|🟢|Cindy [Raw Hem]{"entity": "sf_apparel_hem__raw"} [Straight]{"entity": "sf_apparel_product_type__straight"} Jeans|sf_apparel__title_tags|sf_apparel__title_tags|100.0%|✅|
|66|🟢|Mix [Faux Leather]{"entity": "sf_apparel_material__faux_leather"} & [Nylon]{"entity": "sf_apparel_material__nylon"} [Jacket]{"entity": "sf_apparel_product_type__jacket"}|sf_apparel__title_tags|sf_apparel__title_tags|100.0%|✅|
|67|🟢|[Zebra Print]{"entity": "sf_apparel_pattern__animal__zebra"} Caftan Dress|sf_apparel__title_tags|sf_apparel__title_tags|100.0%|✅|
|68|🟢|Heritage Joon Down [Puffer]{"entity": "sf_apparel_product_type__puffer"} [Jacket]{"entity": "sf_apparel_product_type__jacket"}|sf_apparel__title_tags|sf_apparel__title_tags|100.0%|✅|
|69|🟢|[Corduroy]{"entity": "sf_apparel_material__corduroy"} Single Breasted [Blazer]{"entity": "sf_apparel_product_type__blazer"}|sf_apparel__title_tags|sf_apparel__title_tags|100.0%|✅|
|70|🟢|Twizzy [High Rise]{"entity": "sf_apparel_rise__high_rise"} Utility [Ankle]{"entity": "sf_apparel_length__ankle_length"} Jeans|sf_apparel__title_tags|sf_apparel__title_tags|100.0%|✅|
|71|🟢|Ieena [One Shoulder]{"entity": "sf_apparel_neckline__one_shoulder"} [Ruffled]{"entity": "sf_apparel_hem__ruffled"} [Gown]{"entity": "sf_apparel_product_type__gown"}|sf_apparel__title_tags|sf_apparel__title_tags|100.0%|✅|
|72|🟢|Double Breasted [Flannel]{"entity": "sf_apparel_material__flannel"} [Jacket]{"entity": "sf_apparel_product_type__jacket"}|sf_apparel__title_tags|sf_apparel__title_tags|100.0%|✅|
|73|🟢|Chesterfield Single Breasted [Wool]{"entity": "sf_apparel_material__wool"} [Coat]{"entity": "sf_apparel_product_type__coat"}|sf_apparel__title_tags|sf_apparel__title_tags|100.0%|✅|
|74|🟢|Eden Rock [Crocheted]{"entity": "sf_apparel_product_type__crochet"} Minidress|sf_apparel__title_tags|sf_apparel__title_tags|100.0%|✅|
|75|🟢|Directional [Striped]{"entity": "sf_apparel_pattern__stripes"} Knit [Jacket]{"entity": "sf_apparel_product_type__jacket"}|sf_apparel__title_tags|sf_apparel__title_tags|100.0%|✅|
|76|🟢|[Oversized]{"entity": "sf_apparel_fit__oversized"} Double Breasted [Jacket]{"entity": "sf_apparel_product_type__jacket"}|sf_apparel__title_tags|sf_apparel__title_tags|100.0%|✅|
|77|🟢|[Sequins]{"entity": "sf_apparel_embellishments__sequins"} [Floral]{"entity": "sf_apparel_pattern__floral"} [Embroidery]{"entity": "sf_apparel_embellishments__embroidered"} [Blazer]{"entity": "sf_apparel_product_type__blazer"}|sf_apparel__title_tags|sf_apparel__title_tags|100.0%|✅|
|78|🟢|Pauline [Houndstooth]{"entity": "sf_apparel_pattern__houndstooth"} Elongated [Blazer]{"entity": "sf_apparel_product_type__blazer"}|sf_apparel__title_tags|sf_apparel__title_tags|100.0%|✅|
|79|🟢|[Miranda One Shoulder Sash Midi Dress]{"entity": "sf_apparel_neckline__one_shoulder"}|sf_apparel__title_tags|sf_apparel__title_tags|100.0%|✅|
|80|🟢|Cindy [High Rise]{"entity": "sf_apparel_rise__high_rise"} [Distress]{"entity": "sf_apparel_distressing__distressed"} [Ankle]{"entity": "sf_apparel_length__ankle_length"} Jeans|sf_apparel__title_tags|sf_apparel__title_tags|100.0%|✅|
|81|🟢|Margot Cropped [Mid Rise]{"entity": "sf_apparel_rise__mid_rise"} [Girlfriend]{"entity": "sf_apparel_product_type__girlfriend"} Jeans|sf_apparel__title_tags|sf_apparel__title_tags|100.0%|✅|
|82|🟢|Isa [Strapless]{"entity": "sf_apparel_straps__strapless"} [Pencil]{"entity": "sf_apparel_product_type__pencil"} Dress|sf_apparel__title_tags|sf_apparel__title_tags|100.0%|✅|
|83|🟢|[Bubble Hem]{"entity": "sf_apparel_hem__bubble"} [A Line]{"entity": "sf_apparel_fit__a_line"} Dress|sf_apparel__title_tags|sf_apparel__title_tags|100.0%|✅|
|84|🟢|Cox [Paisley]{"entity": "sf_apparel_pattern__paisley"} [Shirred]{"entity": "sf_apparel_product_type__ruched"} Surplice Minidress|sf_apparel__title_tags|sf_apparel__title_tags|100.0%|✅|
|85|🟢|Kimmie [Mid Rise]{"entity": "sf_apparel_rise__mid_rise"} [Straight]{"entity": "sf_apparel_product_type__straight"} Jeans|sf_apparel__title_tags|sf_apparel__title_tags|100.0%|✅|
|86|🟢|Marcie [Animal Print]{"entity": "sf_apparel_pattern__animal"} Silk Blend Minidress|sf_apparel__title_tags|sf_apparel__title_tags|100.0%|✅|
|87|🟢|Ieena [Beaded]{"entity": "sf_apparel_embellishments__beaded"} [A Line]{"entity": "sf_apparel_fit__a_line"} [Gown]{"entity": "sf_apparel_product_type__gown"}|sf_apparel__title_tags|sf_apparel__title_tags|100.0%|✅|
|88|🟢|Chaz [Faux Leather]{"entity": "sf_apparel_material__faux_leather"} [Bomber]{"entity": "sf_apparel_product_type__bomber"} [Jacket]{"entity": "sf_apparel_product_type__jacket"}|sf_apparel__title_tags|sf_apparel__title_tags|100.0%|✅|
|89|🟢|[Baggy]{"entity": "sf_apparel_product_type__baggy"} Puff Pocket [Cargo Jeans]{"entity": "sf_apparel_pocket_type__cargo_pockets"}|sf_apparel__title_tags|sf_apparel__title_tags|100.0%|✅|
|90|🟢|[Sequined]{"entity": "sf_apparel_embellishments__sequins"} Racerback [Column]{"entity": "sf_apparel_fit__straight_fit"} [Gown]{"entity": "sf_apparel_product_type__gown"}|sf_apparel__title_tags|sf_apparel__title_tags|100.0%|✅|
|91|🟢|[Floral]{"entity": "sf_apparel_pattern__floral"} [High Neck]{"entity": "sf_apparel_neckline__high_neck"} Flutter Sleeve [Gown]{"entity": "sf_apparel_product_type__gown"}|sf_apparel__title_tags|sf_apparel__title_tags|100.0%|✅|
|92|🟢|Keri [Floral]{"entity": "sf_apparel_pattern__floral"} [Vegan]{"entity": "sf_apparel_sustainability__vegan"} Leather Varsity [Jacket]{"entity": "sf_apparel_product_type__jacket"}|sf_apparel__title_tags|sf_apparel__title_tags|100.0%|✅|
|93|🟢|[Sequined]{"entity": "sf_apparel_embellishments__sequins"} [Beaded]{"entity": "sf_apparel_embellishments__beaded"} Tulle [Gown]{"entity": "sf_apparel_product_type__gown"}|sf_apparel__title_tags|sf_apparel__title_tags|100.0%|✅|
|94|🟢|[Sequined]{"entity": "sf_apparel_embellishments__sequins"} [Elbow Sleeve]{"entity": "sf_apparel_sleeve_length__mid_sleeves__elbow_sleeves"} Column [Gown]{"entity": "sf_apparel_product_type__gown"}|sf_apparel__title_tags|sf_apparel__title_tags|100.0%|✅|
|95|🟢|Theodora [Boxy]{"entity": "sf_apparel_fit__relaxed"} [Striped]{"entity": "sf_apparel_pattern__stripes"} Dress|sf_apparel__title_tags|sf_apparel__title_tags|100.0%|✅|
|96|🟢|Bishop Sleeve Wrap [Belted]{"entity": "sf_apparel_waist__belt"} Flowy [Gown]{"entity": "sf_apparel_product_type__gown"}|sf_apparel__title_tags|sf_apparel__title_tags|100.0%|✅|
|97|🟢|Taylor [High Rise]{"entity": "sf_apparel_rise__high_rise"} [Wide Leg]{"entity": "sf_apparel_product_type__wide"} Jeans|sf_apparel__title_tags|sf_apparel__title_tags|100.0%|✅|
|98|🟢|[Solid]{"entity": "sf_apparel_pattern__solid"} Crepe [Embroidered]{"entity": "sf_apparel_embellishments__embroidered"} Topper|sf_apparel__title_tags|sf_apparel__title_tags|100.0%|✅|
|99|🟢|Embellished [Cap Sleeve Dress]{"entity": "sf_apparel_sleeve_style__cap"}|sf_apparel__title_tags|sf_apparel__title_tags|100.0%|✅|
|100|🟢|Yuriko [Shawl Lapel]{"entity": "sf_apparel_collar__shawl"} [Jacket]{"entity": "sf_apparel_product_type__jacket"}|sf_apparel__title_tags|sf_apparel__title_tags|100.0%|✅|
|101|🟢|Vera [Embroidered]{"entity": "sf_apparel_embellishments__embroidered"} [Camouflage]{"entity": "sf_apparel_pattern__camouflage"} [Denim]{"entity": "sf_apparel_material__denim"} [Jacket]{"entity": "sf_apparel_product_type__jacket"}|sf_apparel__title_tags|sf_apparel__title_tags|100.0%|✅|
|102|🟢|Aspen [Cable Knit]{"entity": "sf_apparel_material__cable_knit"} Sweater [Jacket]{"entity": "sf_apparel_product_type__jacket"}|sf_apparel__title_tags|sf_apparel__title_tags|100.0%|✅|
|103|🟢|Harvey [Crewneck]{"entity": "sf_apparel_neckline__roundneck__crewneck"} Retro Tiger [Sweatshirt]{"entity": "sf_apparel_product_type__sweatshirt"}|sf_apparel__title_tags|sf_apparel__title_tags|100.0%|✅|
|104|🟢|[Viscose]{"entity": "sf_apparel_material__viscose"} Crepe Tank [Midi]{"entity": "sf_apparel_length__midi"} Dress|sf_apparel__title_tags|sf_apparel__title_tags|100.0%|✅|
|105|🟢|Embellshed [Short Sleeve]{"entity": "sf_apparel_sleeve_length__short_sleeves"} Column Dress|sf_apparel__title_tags|sf_apparel__title_tags|100.0%|✅|
|106|🟢|Ieena Embellished [Scoopneck]{"entity": "sf_apparel_neckline__roundneck__scoop_neck"} [Sheath]{"entity": "sf_apparel_product_type__sheath"} [Gown]{"entity": "sf_apparel_product_type__gown"}|sf_apparel__title_tags|sf_apparel__title_tags|99.9%|✅|
|107|🟢|Alena [Fringe]{"entity": "sf_apparel_product_type__fringe"} [Sheath]{"entity": "sf_apparel_product_type__sheath"} Dress|sf_apparel__title_tags|sf_apparel__title_tags|99.9%|✅|
|108|🟢|Drop Square [Tie Dye]{"entity": "sf_apparel_pattern__abstract"} [Sweatshirt]{"entity": "sf_apparel_product_type__sweatshirt"}|sf_apparel__title_tags|sf_apparel__title_tags|99.9%|✅|
|109|🟢|Mya [Flap Pocket]{"entity": "sf_apparel_pocket_type__flap_pockets"} [Vegan Leather]{"entity": "sf_apparel_material__faux_leather"} [Blazer]{"entity": "sf_apparel_product_type__blazer"}|sf_apparel__title_tags|sf_apparel__title_tags|99.9%|✅|
|110|🟢|[Ruched]{"entity": "sf_apparel_product_type__ruched"} [Drawstring]{"entity": "sf_apparel_waist__drawstring"} [Cutout]{"entity": "sf_apparel_product_type__cutout"} Dress|sf_apparel__title_tags|sf_apparel__title_tags|99.9%|✅|
|111|🟢|[Silk]{"entity": "sf_apparel_material__silk"} [Leopard]{"entity": "sf_apparel_pattern__animal__leopard"} Slip Minidress|sf_apparel__title_tags|sf_apparel__title_tags|99.9%|✅|
|112|🟢|Ieena [Jersey]{"entity": "sf_apparel_material__jersey"} [Asymmetric]{"entity": "sf_apparel_product_type__asymmetrical"} [Gown]{"entity": "sf_apparel_product_type__gown"}|sf_apparel__title_tags|sf_apparel__title_tags|99.9%|✅|
|113|🟢|Kimmie [Mid Rise]{"entity": "sf_apparel_rise__mid_rise"} [Bootcut]{"entity": "sf_apparel_product_type__bootcut"} Jeans|sf_apparel__title_tags|sf_apparel__title_tags|99.9%|✅|
|114|🟢|[Cashmere]{"entity": "sf_apparel_material__cashmere"} Cape [Turtleneck]{"entity": "sf_apparel_neckline__high_neck__turtleneck"} [Minidress]{"entity": "sf_apparel_length__mini"}|sf_apparel__title_tags|sf_apparel__title_tags|99.9%|✅|
|115|🟢|Palm [Textured]{"entity": "sf_apparel_pattern__dot"} [Dot Minidress]{"entity": "sf_apparel_length__mini"}|sf_apparel__title_tags|sf_apparel__title_tags|99.9%|✅|
|116|🟢|Dickey [Long]{"entity": "sf_apparel_length__long"} Tailored [Jacket]{"entity": "sf_apparel_product_type__jacket"}|sf_apparel__title_tags|sf_apparel__title_tags|99.9%|✅|
|117|🟢|[Boat Neck]{"entity": "sf_apparel_neckline__roundneck__boat_neck"} Rib Knit [Minidress]{"entity": "sf_apparel_length__mini"}|sf_apparel__title_tags|sf_apparel__title_tags|99.9%|✅|
|118|🟢|Krishna [Croc Embossed]{"entity": "sf_apparel_pattern__animal__crocodile"} [Vegan Leather]{"entity": "sf_apparel_material__faux_leather"} [Crop]{"entity": "sf_apparel_length__cropped"} Moto [Jacket]{"entity": "sf_apparel_product_type__jacket"}|sf_apparel__title_tags|sf_apparel__title_tags|99.9%|✅|
|119|🟢|[Floral]{"entity": "sf_apparel_pattern__floral"} [Jacquard]{"entity": "sf_apparel_pattern__jacquard"} [Cropped]{"entity": "sf_apparel_length__cropped"} [Jacket]{"entity": "sf_apparel_product_type__jacket"}|sf_apparel__title_tags|sf_apparel__title_tags|99.9%|✅|
|120|🟢|Embellished [Rose Applique]{"entity": "sf_apparel_embellishments__appliquéd"} [Gown]{"entity": "sf_apparel_product_type__gown"}|sf_apparel__title_tags|sf_apparel__title_tags|99.9%|✅|
|121|🟢|[Jersey]{"entity": "sf_apparel_material__jersey"} [Halterneck]{"entity": "sf_apparel_neckline__halter"} [Gown]{"entity": "sf_apparel_product_type__gown"}|sf_apparel__title_tags|sf_apparel__title_tags|99.9%|✅|
|122|🟢|Le Mini Boot Mid Rise [Stretch]{"entity": "sf_apparel_stretch_type__stretch"} [Flare]{"entity": "sf_apparel_product_type__flare"} Jeans|sf_apparel__title_tags|sf_apparel__title_tags|99.9%|✅|
|123|🟢|Iggy [Plaid]{"entity": "sf_apparel_pattern__plaid"} [Ruched]{"entity": "sf_apparel_product_type__ruched"} [Maxi]{"entity": "sf_apparel_length__maxi"} Dress|sf_apparel__title_tags|sf_apparel__title_tags|99.8%|✅|
|124|🟢|[Notch]{"entity": "sf_apparel_collar__lapel__notch"} [Lapel]{"entity": "sf_apparel_collar__lapel"} [Blazer]{"entity": "sf_apparel_product_type__blazer"}|sf_apparel__title_tags|sf_apparel__description_tags|99.8%|❌|
|125|🟢|The Insider [Frayed Hem]{"entity": "sf_apparel_distressing__frayed"} [Cropped]{"entity": "sf_apparel_length__cropped"} Jeans|sf_apparel__title_tags|sf_apparel__title_tags|99.8%|✅|
|126|🟢|[Fitted]{"entity": "sf_apparel_fit__slim"} [Denim]{"entity": "sf_apparel_material__denim"} [Blazer]{"entity": "sf_apparel_product_type__blazer"}|sf_apparel__title_tags|sf_apparel__title_tags|99.8%|✅|
|127|🟢|Isha [Trench Coat]{"entity": "sf_apparel_product_type__trench"}|sf_apparel__title_tags|sf_apparel__title_tags|99.8%|✅|
|128|🟢|[Bell Sleeve]{"entity": "sf_apparel_sleeve_style__bell"} [Lace]{"entity": "sf_apparel_material__lace"} [Minidress]{"entity": "sf_apparel_length__mini"}|sf_apparel__title_tags|sf_apparel__description_tags|99.8%|❌|
|129|🟢|The [Mom]{"entity": "sf_apparel_product_type__mom"} Jeans|sf_apparel__title_tags|sf_apparel__title_tags|99.8%|✅|
|130|🟢|[Sequined]{"entity": "sf_apparel_embellishments__sequins"} [Half Sleeve]{"entity": "sf_apparel_sleeve_length__mid_sleeves"} [Gown]{"entity": "sf_apparel_product_type__gown"}|sf_apparel__title_tags|sf_apparel__title_tags|99.8%|✅|
|131|🟢|[Collarless]{"entity": "sf_apparel_collar__collarless"} [Wool]{"entity": "sf_apparel_material__wool"} [Jacket]{"entity": "sf_apparel_product_type__jacket"}|sf_apparel__title_tags|sf_apparel__title_tags|99.8%|✅|
|132|🟢|[Sateen]{"entity": "sf_apparel_material__satin"} [Square Neck]{"entity": "sf_apparel_neckline__square"} [Midi Dress]{"entity": "sf_apparel_length__midi"}|sf_apparel__title_tags|sf_apparel__title_tags|99.8%|✅|
|133|🟢|Gathered [Semi Sheer]{"entity": "sf_apparel_embellishments__semi_sheer"} [Floral]{"entity": "sf_apparel_pattern__floral"} [Midi Dress]{"entity": "sf_apparel_length__midi"}|sf_apparel__title_tags|sf_apparel__title_tags|99.7%|✅|
|134|🟢|1996 Nuptse [Down]{"entity": "sf_apparel_product_type__down_jacket"} [Parka]{"entity": "sf_apparel_product_type__parka"} [Coat]{"entity": "sf_apparel_product_type__coat"}|sf_apparel__title_tags|sf_apparel__title_tags|99.7%|✅|
|135|🟢|Luv [Floral Printed]{"entity": "sf_apparel_pattern__floral"} [Shift Dress]{"entity": "sf_apparel_product_type__shift"}|sf_apparel__title_tags|sf_apparel__title_tags|99.7%|✅|
|136|🟢|[Sequined]{"entity": "sf_apparel_embellishments__sequins"} [Body con]{"entity": "sf_apparel_fit__bodycon"} [Mini]{"entity": "sf_apparel_length__mini"} Dress|sf_apparel__title_tags|sf_apparel__title_tags|99.6%|✅|
|137|🟢|Renada [Twist Front]{"entity": "sf_apparel_product_type__tie_front"} [Midi]{"entity": "sf_apparel_length__midi"} Dress|sf_apparel__title_tags|sf_apparel__title_tags|99.6%|✅|
|138|🟢|[Sequin]{"entity": "sf_apparel_embellishments__sequins"} [Sleeveless]{"entity": "sf_apparel_sleeve_length__sleeveless"} [Sheath]{"entity": "sf_apparel_product_type__sheath"} [Gown]{"entity": "sf_apparel_product_type__gown"}|sf_apparel__title_tags|sf_apparel__title_tags|99.6%|✅|
|139|🟢|[Cheetah Print]{"entity": "sf_apparel_pattern__animal__cheetah"} Gathered [Shift]{"entity": "sf_apparel_product_type__shift"} Dress|sf_apparel__title_tags|sf_apparel__title_tags|99.6%|✅|
|140|🟢|[Denim]{"entity": "sf_apparel_material__denim"} [Logo Cuff]{"entity": "sf_apparel_pattern__graphic__logo"} Trucker [Jacket]{"entity": "sf_apparel_product_type__jacket"}|sf_apparel__title_tags|sf_apparel__title_tags|99.5%|✅|
|141|🟢|Enola [Cropped]{"entity": "sf_apparel_length__cropped"} [Denim]{"entity": "sf_apparel_material__denim"} [Jacket]{"entity": "sf_apparel_product_type__jacket"}|sf_apparel__title_tags|sf_apparel__title_tags|99.5%|✅|
|142|🟢|[Beaded]{"entity": "sf_apparel_embellishments__beaded"} [Empire Waist]{"entity": "sf_apparel_waist__empire"} [Gown]{"entity": "sf_apparel_product_type__gown"}|sf_apparel__title_tags|sf_apparel__title_tags|99.4%|✅|
|143|🟢|Ieena [Satin]{"entity": "sf_apparel_material__satin"} [V Neck]{"entity": "sf_apparel_neckline__v_neck"} [Gown]{"entity": "sf_apparel_product_type__gown"}|sf_apparel__title_tags|sf_apparel__title_tags|99.3%|✅|
|144|🟢|[High Rise]{"entity": "sf_apparel_rise__high_rise"} [Stretch]{"entity": "sf_apparel_stretch_type__stretch"} [Slim]{"entity": "sf_apparel_product_type__slim"} Kick Flare Jeans|sf_apparel__title_tags|sf_apparel__title_tags|99.2%|✅|
|145|🟢|Marcy [Floral]{"entity": "sf_apparel_pattern__floral"} [Cut Out]{"entity": "sf_apparel_product_type__cutout"} [Minidress]{"entity": "sf_apparel_length__mini"}|sf_apparel__title_tags|sf_apparel__title_tags|99.1%|✅|
|146|🟢|[Collared]{"entity": "sf_apparel_neckline__collared"} Faux Wrap Bishop Sleeve [Midi Dress]{"entity": "sf_apparel_length__midi"}|sf_apparel__title_tags|sf_apparel__title_tags|99.1%|✅|
|147|🟢|[Mock Turtleneck]{"entity": "sf_apparel_neckline__high_neck__mock"} [Metallic]{"entity": "sf_apparel_pattern__metallic"} Knit [Midi Dress]{"entity": "sf_apparel_length__midi"}|sf_apparel__title_tags|sf_apparel__title_tags|99.1%|✅|
|148|🟢|Sketched Leaves [Linen Blend]{"entity": "sf_apparel_material_composition__blend"} [Midi Dress]{"entity": "sf_apparel_length__midi"}|sf_apparel__title_tags|sf_apparel__title_tags|99.0%|✅|
|149|🟢|[Floral]{"entity": "sf_apparel_pattern__floral"} [Bead Embellished]{"entity": "sf_apparel_embellishments__beaded"} [Ruffle]{"entity": "sf_apparel_product_type__ruffle"} [Gown]{"entity": "sf_apparel_product_type__gown"}|sf_apparel__title_tags|sf_apparel__title_tags|99.0%|✅|
|150|🟢|The Dazzler [Printed]{"entity": "sf_apparel_pattern__patterned"} [Skinny]{"entity": "sf_apparel_product_type__skinny"} Jeans|sf_apparel__title_tags|sf_apparel__title_tags|99.0%|✅|
|151|🟢|Hilary [Faux Fur]{"entity": "sf_apparel_material__faux_fur"} [Jacket]{"entity": "sf_apparel_product_type__jacket"}|sf_apparel__title_tags|sf_apparel__title_tags|98.9%|✅|
|152|🟢|[Belted]{"entity": "sf_apparel_waist__belt"} [Cargo]{"entity": "sf_apparel_pocket_type__pocket"} [Mini Shirtdress]{"entity": "sf_apparel_length__mini"}|sf_apparel__title_tags|sf_apparel__title_tags|98.9%|✅|
|153|🟢|[Gingham]{"entity": "sf_apparel_pattern__gingham"} Ring [Cut Out]{"entity": "sf_apparel_product_type__cutout"} [Midi Dress]{"entity": "sf_apparel_length__midi"}|sf_apparel__title_tags|sf_apparel__title_tags|98.6%|✅|
|154|🟢|Grizzo [Studded]{"entity": "sf_apparel_embellishments__studs"} [Denim]{"entity": "sf_apparel_material__denim"} [Jacket]{"entity": "sf_apparel_product_type__jacket"}|sf_apparel__title_tags|sf_apparel__title_tags|98.5%|✅|
|155|🟢|[Sequined]{"entity": "sf_apparel_embellishments__sequins"} [Mesh]{"entity": "sf_apparel_embellishments__mesh"} [Zip Front]{"entity": "sf_apparel_closure__zipper__front_zipper"} [Gown]{"entity": "sf_apparel_product_type__gown"}|sf_apparel__title_tags|sf_apparel__description_tags|98.5%|❌|
|156|🟢|Theodora [Floral]{"entity": "sf_apparel_pattern__floral"} [Caftan]{"entity": "sf_apparel_product_type__kimono"} Dress|sf_apparel__title_tags|sf_apparel__title_tags|98.3%|✅|
|157|🟢|Tailored [Vest]{"entity": "sf_apparel_product_type__vest"} [Top]{"entity": "sf_apparel_product_type__vest"}|sf_apparel__title_tags|sf_apparel__description_tags|98.3%|❌|
|158|🟢|Fabulouss [Long Sleeve]{"entity": "sf_apparel_sleeve_length__long_sleeves"} Pleated [Plus Size]{"entity": "sf_apparel_size_category__plus_size"} [Gown]{"entity": "sf_apparel_product_type__gown"}|sf_apparel__title_tags|sf_apparel__title_tags|98.2%|✅|
|159|🟢|[Sequined]{"entity": "sf_apparel_embellishments__sequins"} [Puff Sleeve]{"entity": "sf_apparel_sleeve_style__puff"} [Sheath]{"entity": "sf_apparel_product_type__sheath"} [Gown]{"entity": "sf_apparel_product_type__gown"}|sf_apparel__title_tags|sf_apparel__title_tags|97.7%|✅|
|160|🟢|[Cocktail]{"entity": "sf_apparel_product_type__cocktail"} [Floral]{"entity": "sf_apparel_pattern__floral"} [Midi Dress]{"entity": "sf_apparel_length__midi"}|sf_apparel__title_tags|sf_apparel__title_tags|97.5%|✅|
|161|🟢|Ryliana [Floral]{"entity": "sf_apparel_pattern__floral"} [Chiffon]{"entity": "sf_apparel_material__chiffon"} [Maxi]{"entity": "sf_apparel_length__maxi"} Dress|sf_apparel__title_tags|sf_apparel__title_tags|97.0%|✅|
|162|🟢|The Wrapper [Elasticized]{"entity": "sf_apparel_waist__elastic"} [Ankle]{"entity": "sf_apparel_length__ankle_length"} Jeans|sf_apparel__title_tags|sf_apparel__title_tags|96.4%|✅|
|163|🟢|[One Shoulder]{"entity": "sf_apparel_neckline__one_shoulder"} [Jersey]{"entity": "sf_apparel_material__jersey"} [Ruched]{"entity": "sf_apparel_product_type__ruched"} [Side Slit]{"entity": "sf_apparel_slit__side_slit"} [Gown]{"entity": "sf_apparel_product_type__gown"}|sf_apparel__title_tags|sf_apparel__title_tags|96.2%|✅|
|164|🟢|[Floral]{"entity": "sf_apparel_pattern__floral"} [Denim]{"entity": "sf_apparel_material__denim"} [Long Sleeve]{"entity": "sf_apparel_sleeve_length__long_sleeves"} [Minidress]{"entity": "sf_apparel_length__mini"}|sf_apparel__title_tags|sf_apparel__description_tags|96.1%|❌|
|165|🟢|Georgina [Peak]{"entity": "sf_apparel_collar__lapel__peak"} [Single Button Blazer]{"entity": "sf_apparel_closure__button"}|sf_apparel__title_tags|sf_apparel__description_tags|95.9%|❌|
|166|🟢|Woven [Tie Front]{"entity": "sf_apparel_waist__tied"} [Jacket]{"entity": "sf_apparel_product_type__jacket"}|sf_apparel__title_tags|sf_apparel__title_tags|94.8%|✅|
|167|🟢|Suki Colorblocked [Hooded]{"entity": "sf_apparel_neckline__hooded"} [Puffer]{"entity": "sf_apparel_product_type__puffer"}|sf_apparel__title_tags|sf_apparel__title_tags|94.4%|✅|
|168|🟢|Embellished [Puff Sleeve]{"entity": "sf_apparel_sleeve_style__puff"} Wrap Effect [Gown]{"entity": "sf_apparel_product_type__gown"}|sf_apparel__title_tags|sf_apparel__title_tags|93.9%|✅|
|169|🟢|[Maternity]{"entity": "sf_apparel_size_category__maternity"} Skyline [Mid Rise]{"entity": "sf_apparel_rise__mid_rise"} [Skinny]{"entity": "sf_apparel_product_type__skinny"} [Ankle]{"entity": "sf_apparel_length__ankle_length"} Peg Jeans|sf_apparel__title_tags|sf_apparel__title_tags|93.0%|✅|
|170|🟢|Hensley [Chambray]{"entity": "sf_apparel_material__chambray"} [Tie Waist]{"entity": "sf_apparel_waist__belt"} [Shirtdress]{"entity": "sf_apparel_product_type__shirt"}|sf_apparel__title_tags|sf_apparel__title_tags|92.6%|✅|
|171|🟢|Audrey [Belted]{"entity": "sf_apparel_waist__belt"} [Down]{"entity": "sf_apparel_product_type__down_jacket"} [Puffer]{"entity": "sf_apparel_product_type__puffer"} [Jacket]{"entity": "sf_apparel_product_type__jacket"}|sf_apparel__title_tags|sf_apparel__title_tags|90.1%|✅|
|172|🟡|[Python Print]{"entity": "sf_apparel_pattern__animal__snake"} [Long Sleeve]{"entity": "sf_apparel_sleeve_length__long_sleeves"} [Silk]{"entity": "sf_apparel_material__silk"} Shirtdress|sf_apparel__title_tags|sf_apparel__description_tags|89.8%|❌|
|173|🟡|[Three Quarter Length Sleeve]{"entity": "sf_apparel_sleeve_length__mid_sleeves__three_quarter_sleeves"} [Denim]{"entity": "sf_apparel_material__denim"} [Jacket]{"entity": "sf_apparel_product_type__jacket"}|sf_apparel__title_tags|sf_apparel__description_tags|89.7%|❌|
|174|🟡|[Smocked]{"entity": "sf_apparel_product_type__smock"} Waist [Shirtdress]{"entity": "sf_apparel_product_type__shirt"}|sf_apparel__title_tags|sf_apparel__title_tags|87.9%|✅|
|175|🟡|[Off The Shoulder]{"entity": "sf_apparel_neckline__off_the_shoulder"} [Ruffle]{"entity": "sf_apparel_product_type__ruffle"} [Gown]{"entity": "sf_apparel_product_type__gown"}|sf_apparel__title_tags|sf_apparel__title_tags|87.4%|✅|
|176|🟡|[Fay Cardigan]{"entity": "sf_apparel_product_type__sweater"} & [Sweater]{"entity": "sf_apparel_product_type__sweater"} [Two Piece Set]{"entity": "sf_apparel_product_type__two_piece"}|sf_apparel__title_tags|sf_apparel__title_tags|87.1%|✅|
|177|🟡|Alamdea [Asymmetric Zip Jacket]{"entity": "sf_apparel_closure__zipper"}|sf_apparel__title_tags|sf_apparel__title_tags|86.2%|✅|
|178|🟡|Gabriella [Ruched]{"entity": "sf_apparel_product_type__ruched"} [Halter]{"entity": "sf_apparel_neckline__halter"} [Midi Dress]{"entity": "sf_apparel_length__midi"}|sf_apparel__title_tags|sf_apparel__title_tags|85.9%|✅|
|179|🟡|Gaia [Cowl]{"entity": "sf_apparel_neckline__cowl_neck"} [Satin]{"entity": "sf_apparel_material__satin"} [Midi Dress]{"entity": "sf_apparel_length__midi"}|sf_apparel__title_tags|sf_apparel__title_tags|83.3%|✅|
|180|🟡|[One Shoulder]{"entity": "sf_apparel_neckline__one_shoulder"} [High Slit]{"entity": "sf_apparel_slit__front_slit"} [Cocktail Dress]{"entity": "sf_apparel_product_type__cocktail"}|sf_apparel__title_tags|sf_apparel__title_tags|83.1%|✅|
|181|🟡|Sunview [Single Button Blazer]{"entity": "sf_apparel_closure__button"}|sf_apparel__title_tags|sf_apparel__description_tags|78.5%|❌|
|182|🟡|[Maternity]{"entity": "sf_apparel_size_category__maternity"} [Ankle]{"entity": "sf_apparel_length__ankle_length"} [Skinny]{"entity": "sf_apparel_product_type__skinny"} [Faded]{"entity": "sf_apparel_wash__faded"} Jeans|sf_apparel__title_tags|sf_apparel__title_tags|75.6%|✅|
|183|🟡|[Long Sleeve]{"entity": "sf_apparel_sleeve_length__long_sleeves"} Draped [Keyhole]{"entity": "sf_apparel_neckline__keyhole"} [Gown]{"entity": "sf_apparel_product_type__gown"}|sf_apparel__title_tags|sf_apparel__description_tags|73.0%|❌|
|184|🟠|leena [One Sleeve]{"entity": "sf_apparel_sleeve_style__one_sleeve"} [Cut Out]{"entity": "sf_apparel_product_type__cutout"} [Satin]{"entity": "sf_apparel_material__satin"} [Gown]{"entity": "sf_apparel_product_type__gown"}|sf_apparel__title_tags|sf_apparel__title_tags|69.5%|✅|
|185|🟠|[Sweetheart]{"entity": "sf_apparel_neckline__sweetheart"} [Long Sleeve]{"entity": "sf_apparel_sleeve_length__long_sleeves"} Dress|sf_apparel__title_tags|sf_apparel__title_tags|69.4%|✅|
|186|🟠|Lucy [Cotton]{"entity": "sf_apparel_material__cotton"} [Fleece]{"entity": "sf_apparel_material__fleece"} [Hoodie]{"entity": "sf_apparel_product_type__hoodie"}|sf_apparel__title_tags|sf_apparel__title_tags|68.2%|✅|
|187|🟠|[Snap Front]{"entity": "sf_apparel_closure__snap"} Cotton [Blend]{"entity": "sf_apparel_material_composition__blend"} [Blazer]{"entity": "sf_apparel_product_type__blazer"}|sf_apparel__title_tags|sf_apparel__description_tags|66.0%|❌|
|188|🟠|[Cashmere]{"entity": "sf_apparel_material__cashmere"} [Bell Sleeve]{"entity": "sf_apparel_sleeve_style__bell"} [A Line]{"entity": "sf_apparel_fit__a_line"} Dress|sf_apparel__title_tags|sf_apparel__title_tags|65.3%|✅|
|189|🟠|[Cotton Blend]{"entity": "sf_apparel_material_composition__blend"} [Logo]{"entity": "sf_apparel_pattern__graphic__logo"} [Sweatshirt]{"entity": "sf_apparel_product_type__sweatshirt"}|sf_apparel__title_tags|sf_apparel__description_tags|61.8%|❌|
|190|🟠|[Silk]{"entity": "sf_apparel_material__silk"} Twisted [Short Sleeve]{"entity": "sf_apparel_sleeve_length__short_sleeves"} [Gown]{"entity": "sf_apparel_product_type__gown"}|sf_apparel__title_tags|sf_apparel__title_tags|59.7%|✅|
|191|🟠|[V Neck]{"entity": "sf_apparel_neckline__v_neck"} [Bow]{"entity": "sf_apparel_closure__bow"} [Split Hem]{"entity": "sf_apparel_hem__split_hem"} [Knee Length]{"entity": "sf_apparel_length__midi"} [A Line]{"entity": "sf_apparel_fit__a_line"} [Midi Dress]{"entity": "sf_apparel_length__midi"}|sf_apparel__title_tags|sf_apparel__description_tags|51.4%|❌|

### Sentences with problems
Table with the sentences that were not understood correctly by the model.

|#||Text|Intent|Predicted intent|Confidence|Understood|
|:-:|-|-|-|-|-|-|
|1|🟢|[Notch]{"entity": "sf_apparel_collar__lapel__notch"} [Lapel]{"entity": "sf_apparel_collar__lapel"} [Blazer]{"entity": "sf_apparel_product_type__blazer"}|sf_apparel__title_tags|sf_apparel__description_tags|99.8%|❌|
|2|🟢|[Bell Sleeve]{"entity": "sf_apparel_sleeve_style__bell"} [Lace]{"entity": "sf_apparel_material__lace"} [Minidress]{"entity": "sf_apparel_length__mini"}|sf_apparel__title_tags|sf_apparel__description_tags|99.8%|❌|
|3|🟢|[Sequined]{"entity": "sf_apparel_embellishments__sequins"} [Mesh]{"entity": "sf_apparel_embellishments__mesh"} [Zip Front]{"entity": "sf_apparel_closure__zipper__front_zipper"} [Gown]{"entity": "sf_apparel_product_type__gown"}|sf_apparel__title_tags|sf_apparel__description_tags|98.5%|❌|
|4|🟢|Tailored [Vest]{"entity": "sf_apparel_product_type__vest"} [Top]{"entity": "sf_apparel_product_type__vest"}|sf_apparel__title_tags|sf_apparel__description_tags|98.3%|❌|
|5|🟢|[Floral]{"entity": "sf_apparel_pattern__floral"} [Denim]{"entity": "sf_apparel_material__denim"} [Long Sleeve]{"entity": "sf_apparel_sleeve_length__long_sleeves"} [Minidress]{"entity": "sf_apparel_length__mini"}|sf_apparel__title_tags|sf_apparel__description_tags|96.1%|❌|
|6|🟢|Georgina [Peak]{"entity": "sf_apparel_collar__lapel__peak"} [Single Button Blazer]{"entity": "sf_apparel_closure__button"}|sf_apparel__title_tags|sf_apparel__description_tags|95.9%|❌|
|7|🟡|[Python Print]{"entity": "sf_apparel_pattern__animal__snake"} [Long Sleeve]{"entity": "sf_apparel_sleeve_length__long_sleeves"} [Silk]{"entity": "sf_apparel_material__silk"} Shirtdress|sf_apparel__title_tags|sf_apparel__description_tags|89.8%|❌|
|8|🟡|[Three Quarter Length Sleeve]{"entity": "sf_apparel_sleeve_length__mid_sleeves__three_quarter_sleeves"} [Denim]{"entity": "sf_apparel_material__denim"} [Jacket]{"entity": "sf_apparel_product_type__jacket"}|sf_apparel__title_tags|sf_apparel__description_tags|89.7%|❌|
|9|🟡|Sunview [Single Button Blazer]{"entity": "sf_apparel_closure__button"}|sf_apparel__title_tags|sf_apparel__description_tags|78.5%|❌|
|10|🟡|[Long Sleeve]{"entity": "sf_apparel_sleeve_length__long_sleeves"} Draped [Keyhole]{"entity": "sf_apparel_neckline__keyhole"} [Gown]{"entity": "sf_apparel_product_type__gown"}|sf_apparel__title_tags|sf_apparel__description_tags|73.0%|❌|
|11|🟠|[Snap Front]{"entity": "sf_apparel_closure__snap"} Cotton [Blend]{"entity": "sf_apparel_material_composition__blend"} [Blazer]{"entity": "sf_apparel_product_type__blazer"}|sf_apparel__title_tags|sf_apparel__description_tags|66.0%|❌|
|12|🟠|[Cotton Blend]{"entity": "sf_apparel_material_composition__blend"} [Logo]{"entity": "sf_apparel_pattern__graphic__logo"} [Sweatshirt]{"entity": "sf_apparel_product_type__sweatshirt"}|sf_apparel__title_tags|sf_apparel__description_tags|61.8%|❌|
|13|🟠|[V Neck]{"entity": "sf_apparel_neckline__v_neck"} [Bow]{"entity": "sf_apparel_closure__bow"} [Split Hem]{"entity": "sf_apparel_hem__split_hem"} [Knee Length]{"entity": "sf_apparel_length__midi"} [A Line]{"entity": "sf_apparel_fit__a_line"} [Midi Dress]{"entity": "sf_apparel_length__midi"}|sf_apparel__title_tags|sf_apparel__description_tags|51.4%|❌|

## Core <a name='core'></a>
Section that discusses metrics about bot responses and actions.

### Metrics
Table with bot core metrics.

|#||Response|Precision|Recall|F1 Score|Number of occurrences|
|:-:|-|-|-|-|-|-|
|1|🟢|utter_happy|100.0%|100.0%|100.0%|3|
|2|🟢|utter_iamabot|100.0%|100.0%|100.0%|1|
|3|🟢|utter_goodbye|100.0%|100.0%|100.0%|4|
|4|🟢|utter_greet|100.0%|100.0%|100.0%|5|
|5|🟢|utter_cheer_up|100.0%|100.0%|100.0%|3|
|6|🟢|action_listen|100.0%|100.0%|100.0%|16|
|7|🟢|utter_did_that_help|100.0%|100.0%|100.0%|3|
### Confusion Matrix
![Confusion Matrix](results/story_confusion_matrix.png 'Confusion Matrix')

## E2E Coverage <a name='e2e'></a>
Section that shows data from intents and responses that aren't covered by end-to-end tests.

### Not covered elements
List with not covered elements by end-to-end tests.

#### Intents
 - sf_apparel__description_tags
 - sf_apparel__title_tags
 - sf_apparel__NO_MATCH

#### Actions
 - (no elements not covered)

Total number of elements: 4

Total number of not covered elements: 3

Total number of excluded elements: 0

Coverage rate: 25.0% (🔴)


##### Generated by rasa-model-report v1.5.0, collaborative open-source project for Rasa projects. Github repository at this [link](https://github.com/brunohjs/rasa-model-report).
