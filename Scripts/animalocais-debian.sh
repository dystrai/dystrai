#!/bin/sh

# Cria contas locais no Debian GNU/Linux com nome de animais em português

cat << 'FIM' | 
🐜,ant,formiga,:ant:
🦡,badger,texugo,:badger:
🦇,bat,morcego,:bat:
🦫,beaver,castor,:beaver:
🪲,beetle,besouro,:beetle:
🐦,bird,passaro,:bird:
🦬,bison,bisao,:bison:
🐡,blowfish,baiacu,:blowfish:
🐃,buffalo,bufalo,:water_buffalo:
🐛,bug,inseto,:bug:
🦋,butterfly,borboleta,:butterfly:
🐫,camel,camelo,:two-hump_camel:
🐈,cat,gato,:cat:
🐤,chick,pintinho,:baby_chick:
🐿️,chipmunk,esquilo,:chipmunk:
🪳,cockroach,barata,:cockroach:
🪸,coral,coral,:coral:
🐄,cow,vaca,:cow:
🦀,crab,caranguejo,:crab:
🦗,cricket,grilo,:cricket:
🐊,crocodile,crocodilo,:crocodile:
🦌,deer,veado,:deer:
🦤,dodo,dodo,:dodo:
🐕,dog,cachorro,:dog:
🐬,dolphin,golfinho,:dolphin:
🕊️,dove,pombo,:dove:
🐪,dromedary,dromedario,:camel:
🦆,duck,pato,:duck:
🦅,eagle,aguia,:eagle:
🐘,elephant,elefante,:elephant:
🐟,fish,peixe,:fish:
🦩,flamingo,flamingo,:flamingo:
🪰,fly,mosca,:fly:
🦒,giraffe,girafa,:giraffe:
🐐,goat,cabra,:goat:
🪿,goose,ganso,:goose:
🦍,gorilla,gorila,:gorilla:
🦔,hedgehog,ourico,:hedgehog:
🦛,hippopotamus,hipopotamo,:hippopotamus:
🐝,honeybee,abelha,:honeybee:
🐎,horse,cavalo,:horse:
🪼,jellyfish,medusa,:jellyfish:
🦘,kangaroo,canguru,:kangaroo:
🐞,ladybeetle,joaninha,:lady_beetle:
🐆,leopard,leopardo,:leopard:
🦎,lizard,lagarto,:lizard:
🦙,llama,llama,:llama:
🦞,lobster,lagosta,:lobster:
🦣,mammoth,mamute,:mammoth:
🐒,monkey,macaco,:monkey:
🦟,mosquito,mosquito,:mosquito:
🐁,mouse,camundongo,:mouse:
🐙,octopus,polvo,:octopus:
🦧,orangutan,orangotango,:orangutan:
🦦,otter,lontra,:otter:
🦉,owl,coruja,:owl:
🐂,ox,boi,:ox:
🦜,parrot,papagaio,:parrot:
🦚,peacock,pavao,:peacock:
🐧,penguin,pinguim,:penguin:
🐖,pig,porco,:pig:
🐩,poodle,poodle,:poodle:
🐇,rabbit,coelho,:rabbit:
🐏,ram,carneiro,:ram:
🐀,rat,rato,:rat:
🦏,rhinoceros,rinoceronte,:rhinoceros:
🐓,rooster,galo,:rooster:
🦕,sauropod,sauropode,:sauropod:
🦂,scorpion,escorpiao,:scorpion:
🦭,seal,foca,:seal:
🐑,sheep,ovelha,:ewe:
🦐,shrimp,camarao,:shrimp:
🦨,skunk,gamba,:skunk:
🦥,sloth,preguica,:sloth:
🐌,snail,caracol,:snail:
🐍,snake,serpente,:snake:
🕷️,spider,aranha,:spider:
🦑,squid,lula,:squid:
🦢,swan,cisne,:swan:
🦖,t-rex,t-rex,:T-Rex:
🐅,tiger,tigre,:tiger:
🦃,turkey,peru,:turkey:
🐢,turtle,tartaruga,:turtle:
🪱,worm,verme,:worm:
🐋,whale,baleia,:whale:
FIM
while IFS=',' read -r emoji english portugues shortcode
    do
        if id "$english" >/dev/null 2>&1; then
            echo "Usuário '$english' já existe."
            continue
        fi

        echo "Criando usuário: $portugues ($english)"

        useradd \
            -m \
            -d "/home/$portugues" \
            -s /bin/zsh \
            -c "${portugues},${english},${emoji}" \
            "$portugues"

        echo "${portugues}:${english}" | chpasswd
        chage -d 0 "${portugues}"

    done
