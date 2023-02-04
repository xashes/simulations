#lang racket

(module+ test
  (require rackunit))

(define max-rows 200)
(define max-cols max-rows)
(define live-cell-pct 0.05)
(define grid-size 4)

(define (make-matrix rows cols [v 0])
  (for/vector ([i rows])
    (make-vector cols v)
    )
  )

;; 随机生成某个模式的初始状态
(define (init-world matrix)
  (for* ([r max-rows]
         [c max-cols])
    (matrix-set! matrix r c (if (< (random) live-cell-pct)
                                1
                                0)))
  matrix
  )

(define (matrix-ref matrix row col)
  (vector-ref (vector-ref matrix row)
              col)
  )

(define (matrix-set! matrix row col v)
  (vector-set! (vector-ref matrix row) col v)
  matrix
  )

(define (get-neighbors matrix row col)
  (let ([left (max 0 (sub1 col))]
        [right (min max-cols (+ 2 col))]
        [top (max 0 (sub1 row))]
        [bottom (min max-rows (+ 2 row))]
        )
    (for*/list ([r (in-range top bottom)]
                [c (in-range left right)]
                #:unless (and (= r row)
                              (= c col))
                )
      (matrix-ref matrix r c)
      ))
  )

(define (live-neighbor-sum matrix row col)
  (apply + (get-neighbors matrix row col))
  )

(define (update-cells! matrix)
  (define neighbor-sum-matrix
    (for/vector ([r max-rows])
      (for/vector ([c max-cols])
        (live-neighbor-sum matrix r c))
      )
    )
  (for ([r (in-range max-rows)])
    (for ([c (in-range max-cols)])
      (let ([nsum (matrix-ref neighbor-sum-matrix r c)])
        (cond
          [(= nsum 3) (matrix-set! matrix r c 1)]
          [(= nsum 2) (void)]
          [else (matrix-set! matrix r c 0)]
          )
        )))
  matrix
  )

(module+ test
  (let-values ([(r1 c1) (values 0 1)]
               [(r2 c2) (values 2 2)])
    (define mt (make-matrix max-rows max-cols))
    (matrix-set! mt r1 c1 1)
    (check-equal? (matrix-ref mt r1 c1) 1)
    (matrix-set! mt r2 c2 1)
    (check-equal? (matrix-ref mt r2 c2) 1)
    (check-equal? (apply + (get-neighbors mt 1 1))
                  2)
    (check-equal? (length (get-neighbors mt 0 0))
                  3)
    (check-equal? (live-neighbor-sum mt 0 0)
                  1)
    )
  )

(require 2htdp/image
         2htdp/universe)

(define width (* grid-size max-cols))
(define height (* grid-size max-rows))

(define (grid-to-pixel x y)
  ;; col is x, row is y
  (values (+ (* x grid-size) (/ grid-size 2))
          (+ (* y grid-size) (/ grid-size 2))
          ))

(define ET-SCENE (empty-scene width height))

(define (render-matrix matrix)
  (for*/fold ([img ET-SCENE])
             ([r max-rows]
              [c max-cols]
              #:when (not (zero? (matrix-ref matrix r c))))
    (let-values ([(x y) (grid-to-pixel c r)])
      (place-image (rectangle grid-size grid-size 'solid 'red)
                    x y
                    img
                    )))
  )

(define (reset matrix)
  (init-world matrix)
  )

(define (key-handler mt akey)
  (cond
    [(key=? akey "r") (reset mt)]
    [else mt]
    )
  )

(module+ main
  (define mt (make-matrix max-rows max-cols))
  (init-world mt)
  (big-bang mt
            [on-tick update-cells! 1/30]
            [to-draw render-matrix]
            [on-key key-handler]
            )
  )
