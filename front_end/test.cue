ref: name: "components/frontend"
description: {

    serv:{
        server:{
            restap:{protocol:"http", port: 8080}
        }
    }
    client: {}
    dubplex: {}
}

//Component probes like a ping
probe: frontend:{
    livenes
}

env:{

    // accesso a un secreto
    HTTP_SERVER_PORT_ENV: value: "\(serv.server.restapi.port)"
}

size: {
    memory: {size:100, unit:"M}
    mincpu: 100
    cpu:{size:200, unit:"m"}
}

//service_artifact.cue
import{
    f".../component/frontend:Component"
}