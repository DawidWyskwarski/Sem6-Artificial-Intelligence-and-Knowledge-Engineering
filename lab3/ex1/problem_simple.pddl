(define (problem package_delivery_simple) 
    (:domain package_delivery_domain)
    
    (:objects
        truck1 - truck
        plane1 - plane
        boat1 - boat
        
        p1 p2 p3 p4 - package
        
        city_A city_B - location
        airport1 airport2 - location
        port1 port2 - location
    )

    (:init
        (= (total-cost) 0)

        (at truck1 city_A)
        (at plane1 airport1)
        (at boat1 port1)
        
        (has truck1 p1)
        (has truck1 p2)
        (has truck1 p3)
        (has truck1 p4)

        (road_connection city_A city_B)
        (road_connection city_B city_A)
        (= (distance city_A city_B) 50)
        (= (distance city_B city_A) 50)

        (road_connection city_A airport1)
        (road_connection airport1 city_A)
        (= (distance city_A airport1) 15)
        (= (distance airport1 city_A) 15)

        (road_connection city_A port1)
        (road_connection port1 city_A)
        (= (distance city_A port1) 20)
        (= (distance port1 city_A) 20)

        (plane_connection airport1 airport2)
        (plane_connection airport2 airport1)
        (= (distance airport1 airport2) 300)
        (= (distance airport2 airport1) 300)
        
        (boat_connection port1 port2)
        (boat_connection port2 port1)
        (= (distance port1 port2) 400)
        (= (distance port2 port1) 400)

        (target p1 city_B)
        (target p2 airport2)
        (target p3 port2)
        (target p4 port2)
    )

    (:goal
        (and
            (delivered p1)
            (delivered p2)
            (delivered p3)
            (delivered p4)
        )
    )
    
    ; (:metric minimize (total-cost))
    (:metric minimize (total-time))
)