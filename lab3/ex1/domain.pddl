(define (domain package_delivery_domain)

    (:requirements :strips :typing :fluents :action-costs :durative-actions)

    (:types 
        location - object
        locatable - object
        package - locatable
        vehicle - locatable
        plane - vehicle
        boat - vehicle
        truck - vehicle
    )

    (:predicates 
        (at ?l - locatable ?dl - location)
        (has ?v - vehicle ?p - package)
        (road_connection ?l1 - location ?l2 - location)
        (boat_connection ?l1 - location ?l2 - location)
        (plane_connection ?l1 - location ?l2 - location)
        (target ?p - package ?l - location)
        (delivered ?p - package)
    )
    
    (:functions
        (total-cost)
        (distance ?l1 - location ?l2 - location)
    )

    ; Package management
    (:durative-action unpack
        :parameters (?v - vehicle ?p - package ?l - location)
        :duration (= ?duration 1)
        :condition (and 
            (over all (at ?v ?l))
            (at start (has ?v ?p))
        )
        :effect (and 
            (at start (not (has ?v ?p)))
            (at end (at ?p ?l))
        )
    )

    (:durative-action pack
        :parameters (?v - vehicle ?p - package ?l - location)
        :duration (= ?duration 1)
        :condition (and 
            (over all (at ?v ?l))
            (at start (at ?p ?l))
        )
        :effect (
            at end (has ?v ?p)
        )
    )

    ; Transportation options
    (:durative-action drive
        :parameters (?t - truck ?from - location ?to - location)
        :duration (= ?duration (* 3 (distance ?from ?to)))
        :condition (and 
            (at start (at ?t ?from))
            (over all (road_connection ?from ?to))
        )
        :effect (and 
            (at start (not (at ?t ?from)))
            (at end (at ?t ?to))
            (at end (increase (total-cost) (* 3 (distance ?from ?to))))
        )
    )
    
    (:durative-action fly
        :parameters (?p - plane ?from - location ?to - location)
        :duration (= ?duration (distance ?from ?to))
        :condition (and 
            (at start (at ?p ?from))
            (over all (plane_connection ?from ?to))
        )
        :effect (and 
            (at start (not (at ?p ?from)))
            (at end (at ?p ?to))
            (at end (increase (total-cost) (* 10 (distance ?from ?to))))
        )
    )

    (:durative-action sail
        :parameters (?b - boat ?from - location ?to - location)
        :duration (= ?duration (* 6 (distance ?from ?to)))
        :condition (and 
            (at start (at ?b ?from))
            (over all (boat_connection ?from ?to))
        )
        :effect (and 
            (at start (not (at ?b ?from)))
            (at end (at ?b ?to))
            (at end (increase (total-cost) (distance ?from ?to)))
        )
    )

    (:action mark_delivered
        :parameters (?p - package ?l - location)
        :precondition (and (target ?p ?l) (at ?p ?l))
        :effect (delivered ?p)
    )
)