# Trabalho SDN Lucas Linhares, Guilherme Sousa

## Parte A

### 1. Saida de `net`

```mininet
mininet> net
h1 h1-eth0:s1-eth1
h2 h2-eth0:s1-eth2
h3 h3-eth0:s1-eth3
s1 lo:  s1-eth1:h1-eth0 s1-eth2:h2-eth0 s1-eth3:h3-eth0
c0
```

```sh
                  +----------------+
                  | Controlador c0 |
                  +----------------+
                          :
                          : OpenFlow
                          :
                  +----------------+
                  |   Switch s1    |
                  +----------------+
                   /      |       \
              eth1       eth2      eth3
                /         |         \
             eth0        eth0       eth0
              /           |           \
        +----------+ +----------+ +----------+
        |    h1    | |    h2    | |    h3    |
        | 10.0.0.1 | | 10.0.0.2 | | 10.0.0.3 |
        +----------+ +----------+ +----------+
```

### 2. Comparação do RTT do pings

| Pacote ICMP | RTT     |
| ----------- | ------- |
| Primeiro    | 0.465ms |
| Segundo     | 0.103ms |
| Terceiro    | 0.123ms |
| Media       | 0.230ms |

O primeiro ping apresentou um RTT aproximadamento quatro vezes superior ao dos seguintes.

Com o encaminhamento reativo, quando o switch recebe um pacote para o qual ainda não possui uma regra de encaminhamento, ele comunica com o controlador (`PACKET_IN`). O controlador determina o caminho de encaminhamento e envia uma regra de encaminhamento para o switch (`FLOW_MOD`).

### 3. Débito medido `iperf`

```mininet
mininet> iperf h1 h2
*** Iperf: testing TCP bandwidth between h1 and h2
*** Results: ['27.7 Gbits/sec', '27.8 Gbits/sec']
```

| Medição  | Débito TCP     |
| -------- | -------------- |
| Primeiro | 27.7 Gbits/sec |
| Segundo  | 27.8 Gbits/sec |

O Mininet utiliza interfaces virtuais e todos os dispositvos da topologia são executados na mesma máquina.
Como os pacotes são encaminhados por software, sem atravessarem interfaces físicas e não foi configurado um limite de laruga de banda, o débito depende principalmente da capacidadade de processamento da máquina.

### 4. Comportamento `pingall` depois de `link s1 h1 down`

```mininet
mininet> link s1 h1 down
mininet> iperf h1 h2
*** Iperf: testing TCP bandwidth between h1 and h2
*** Results: ['31.1 Gbits/sec', '31.2 Gbits/sec']
mininet> link s1 h1 down
mininet> pingall
*** Ping: testing ping reachability
h1 -> X X
h2 -> X h3
h3 -> X h2
*** Results: 66% dropped (2/6 received)
```

Ao executar `pingall` após o link `s1 h1` ser desligado, `h1` fica isolado da rede e não consegue alcançar `h2` ou `h3`. Os hosts `h2` e `h3` continuam conectados, mas não conseguem alcançar `h1`.
