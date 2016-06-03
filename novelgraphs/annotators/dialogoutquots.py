from .annotator import Annotator

#depends on DialogID and QuotationID

def _mark_dialog_without_quotes_ids(table):
    table['DialogOutQuotesID'] = None
    sentences_without_quotes = table.DialogID.notnull() & table.QuotationID.isnull()
    
    table.loc[sentences_without_quotes, 'DialogOutQuotesID'] = table.DialogID

class DialogOutQuotes(Annotator):
    def annotate(self, text):
        _mark_dialog_without_quotes_ids(text.tags)
