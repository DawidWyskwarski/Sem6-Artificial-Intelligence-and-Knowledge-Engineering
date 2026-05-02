(define (domain cleaning-robot)

    (:requirements :strips :typing)

    (:types 
        robot 
        room 
    )

    (:predicates
        (at ?r - robot ?rm - room)
        (dirty ?rm - room)
        (clean ?rm - room)
    )

    (:action move
        :parameters (?r - robot ?from - room ?to - room)
        :precondition (at ?r ?from)
        :effect ( and 
            (not (at ?r ?from)) 
            (at ?r ?to) 
        )
    )
    
    (:action clean
        :parameters (?r - robot ?rm - room)
        :precondition ( and 
            (at ?r ?rm) 
            (dirty ?rm)    
        )
        :effect ( and 
            (at ?r ?rm) 
            (clean ?rm)
            (not (dirty ?rm))
        )
    )
)