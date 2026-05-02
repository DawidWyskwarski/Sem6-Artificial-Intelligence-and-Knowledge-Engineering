(define (problem clean-rooms) 
    (:domain cleaning-robot)
    
    (:objects 
        rumba - robot
        room1 - room
        room2 - room
        room3 - room
    )

    (:init
        (at rumba room1)
        (dirty room1)
        (dirty room2)
        (dirty room3)
    )

    (:goal 
        (and
            (clean room1)
            (clean room2)
            (clean room3)
        )
    )
)
