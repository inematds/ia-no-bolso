# FALHAS

| data | o que quebrou | menor correção | prompt \| infra |
|---|---|---|---|
| 2026-11-14 | celular/: "Falhou: abort" ao ligar a IA num celular real, depois do download | no celular `n_gpu_layers: 0` + tentar n_ctx menor/1 núcleo sem rebaixar | infra |
