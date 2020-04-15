from viewflow import flow
from viewflow.base import this, Flow
from viewflow.flow.views import CreateProcessView, UpdateProcessView
from .models import HelloWorldProcess
from viewflow import frontend


@frontend.register
class HelloWorldFlow(Flow):
    process_class = HelloWorldProcess
    """
    Implementação do evento de inicialização do processo
    """
    start = (
        flow.Start(
            CreateProcessView,
            fields=["text"]
        ).Permission(
            auto_create=True
        ).Next(this.approve)
    )
    """
    Implementação da atividade de aprovação da instância de processo
    """
    approve = (
        flow.View(
            UpdateProcessView,
            fields=["approved"]
        ).Permission(
            auto_create=True
        ).Next(this.check_approve)
    )
    """
    implementação de elemento de decisão exclusiva
    """
    check_approve = (
        flow.If(lambda activation: activation.process.approved)
        .Then(this.send)
        .Else(this.end)
    )

    send = (
        flow.Handler(
            this.send_hello_world_request
        ).Next(this.end)
    )

    end = flow.End()

    def send_hello_world_request(self, activation):
        print(activation.process.text)