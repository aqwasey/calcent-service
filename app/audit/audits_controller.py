from app.audit.audits_model import AuditLog, AuditLogsModel


class AuditLogsController:

    def __init__(self):
        self.mod = AuditLogsModel()

    def write(self, aud: AuditLog):
        result = self.mod.add(aud)
        return result

    def show_today(self, info: dict()):
        # select all the items using no filter
        result = self.mod.today_logs(info)
        if len(result) > 0:
            return result
        return 'No agent log(s) found today.'

    def show_overall(self, info: dict()):
        # select all the items using no filter
        result = self.mod.overall_logs(info)
        if len(result) > 0:
            return result
        return 'No overall agent log(s) found.'
