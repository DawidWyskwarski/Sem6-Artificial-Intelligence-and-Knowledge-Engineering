(define (problem package_delivery_complex) 
    (:domain package_delivery_domain)
    
    (:objects
        truck1 truck2 - truck
        plane1 - plane
        boat1 - boat
        
        p1 p2 p3 p4 - package
        
        city1 airport1 port1 - location
        
        city2_A city2_B airport2 - location
        
        port2 - location
    )

    (:init
        (= (total-cost) 0)

        (at truck1 city1)
        (at plane1 airport1)
        (at boat1 port1)
        (at truck2 airport2)
        
        (has truck1 p1)
        (has truck1 p2)
        (has truck1 p3)
        (has truck1 p4)

        (road_connection city1 airport1)
        (road_connection airport1 city1)
        (= (distance city1 airport1) 15)
        (= (distance airport1 city1) 15)

        (road_connection city1 port1)
        (road_connection port1 city1)
        (= (distance city1 port1) 20)
        (= (distance port1 city1) 20)

        (road_connection airport1 port1)
        (road_connection port1 airport1)
        (= (distance airport1 port1) 10)
        (= (distance port1 airport1) 10)

        (road_connection airport2 city2_A)
        (road_connection city2_A airport2)
        (= (distance airport2 city2_A) 25)
        (= (distance city2_A airport2) 25)

        (road_connection airport2 city2_B)
        (road_connection city2_B airport2)
        (= (distance airport2 city2_B) 30)
        (= (distance city2_B airport2) 30)

        (road_connection city2_A city2_B)
        (road_connection city2_B city2_A)
        (= (distance city2_A city2_B) 15)
        (= (distance city2_B city2_A) 15)

        (plane_connection airport1 airport2)
        (plane_connection airport2 airport1)
        (= (distance airport1 airport2) 400)
        (= (distance airport2 airport1) 400)
        
        (road_connection city1 city2_A)
        (road_connection city2_A city1)
        (= (distance city1 city2_A) 500)
        (= (distance city2_A city1) 500)

        (boat_connection port1 port2)
        (boat_connection port2 port1)
        (= (distance port1 port2) 600)
        (= (distance port2 port1) 600)

        (plane_connection airport1 port2)
        (plane_connection port2 airport1)
        (= (distance airport1 port2) 600)
        (= (distance port2 airport1) 600)

        (target p1 city2_A)
        (target p2 city2_B)
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

    (:metric minimize (total-cost))
    ; (:metric minimize (total-time))
)