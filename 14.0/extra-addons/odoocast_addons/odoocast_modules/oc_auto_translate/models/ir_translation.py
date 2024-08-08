from odoo import fields, models, api, _
from mtranslate import translate
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger()

class IrTranslation(models.Model):
    _inherit = 'ir.translation'
    
    def auto_generate_translation(self):
        for term in self:
            target_language = term.lang.split('_')[0]
            if not term.value:
                text = term.src
                try:
                    chunk_size = 400
                    chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
                    translated_chunks = []
                    for chunk in chunks:
                        translated_chunk = translate(chunk, target_language)
                        if translated_chunk:
                            translated_chunks.append(translated_chunk)
                    if len(translated_chunks) > 0:
                        translated = " ".join(translated_chunks)
                    # translated = translate(text, target_language)
                    if translated:
                        term.sudo().write({
                            'value': translated
                        })
                        term.env.cr.commit()
                except Exception as e:
                    raise UserError('%s, Model: %s, ID: %s' % (e, term._name, term.id))
            
            # translator = Translator(to_lang=target_language)
            # if not term.value:
            #     text = term.src
            #     try:
            #         translated = translator.translate(text)
            #         if translated:
            #             term.update({
            #                 'value': translated
            #             })
            #             term.env.cr.commit()
            #     except Exception as e:
            #         raise UserError('%s, Model: %s, ID: %s' % (e, term._name, term.id))