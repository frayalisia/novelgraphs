from .annotator import Annotator


def _get_dialog_sentence_ids(tags):
    quotation_id_counts = tags.groupby('SentenceID').QuotationID.count()
    return list(quotation_id_counts.index[quotation_id_counts > 0])


def _group_sentences(sentences, max_distance):
    groups = []
    group = None
    for sentence in sentences:
        if group is None:
            group = [sentence, sentence]
        else:
            if sentence - group[1] <= max_distance:
                group[1] = sentence
            else:
                groups.append(group)
                group = [sentence, sentence]
    groups.append(group)
    return groups


def _mark_dialog_ids(tags, dialogs):
    tags['DialogID'] = None
    sentences = tags.groupby('SentenceID')
    for dialog_id, dialog in enumerate(dialogs):
        start_sentence, end_sentence = dialog
        start_id = sentences.indices[start_sentence][0]
        end_id = sentences.indices[end_sentence][-1]
        tags.loc[start_id:end_id, 'DialogID'] = dialog_id


class Dialog(Annotator):
    def annotate(self, text):
        dialog_sentence_ids = _get_dialog_sentence_ids(text.tags)
        dialogs = _group_sentences(dialog_sentence_ids, 3)
        _mark_dialog_ids(text.tags, dialogs)
