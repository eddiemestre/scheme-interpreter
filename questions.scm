; Some utility functions that you may find useful.
(define (map proc items)
  (if (null? items)
      nil
      (cons (proc (car items))
            (map proc (cdr items)))))

(define (filter predicate sequence)
  (cond ((null? sequence) nil)
        ((predicate (car sequence))
         (cons (car sequence)
               (filter predicate (cdr sequence))))
        (else (filter predicate (cdr sequence)))))

(define (accumulate op initial sequence)
  (if (null? sequence)
      initial
      (op (car sequence)
          (accumulate op initial (cdr sequence)))))

; Problem 18

;; Merge two lists LIST1 and LIST2 according to COMP and return
;; the merged lists.
(define (merge comp list1 list2)
    ; *** YOUR CODE HERE ***
       (cond
       ((null? list1) list2)
       ((null? list2) list1)
       ((comp (car list1) (car list2)) (append (list (car list1)) (merge comp (cdr list1) list2)))
       (else (append (list (car list2)) (merge comp (cdr list2) list1)))
       ))


(merge < '(1 5 7 9) '(4 8 10))
; expect (1 4 5 7 8 9 10)
(merge > '(9 7 5 1) '(10 8 4 3))
; expect (10 9 8 7 5 4 3 1)

;; Sort a list of lists of numbers to be in decreasing lexicographic
;; order. Relies on a correct implementation of merge.
(define (sort-lists lsts)
  (if (or (null? lsts) (null? (cdr lsts)))
      lsts
      (let ((sublsts (split lsts)))
        (merge greater-list
               (sort-lists (car sublsts))
               (sort-lists (cdr sublsts))))))

(define (greater-list x y)
  (cond ((null? y) #t)
        ((null? x) #f)
        ((> (car x) (car y)) #t)
        ((> (car y) (car x)) #f)
        (else (greater-list (cdr x) (cdr y)))))

(define (split x)
  (cond ((or (null? x) (null? (cdr x))) (cons x nil))
        (else (let ((sublsts (split (cdr (cdr x)))))
                (cons (cons (car x) (car sublsts))
                      (cons (car (cdr x)) (cdr sublsts)))))))

(merge greater-list '((3 2 1) (1 1) (0)) '((4 0) (3 2 0) (3 2) (1)))
; expect ((4 0) (3 2 1) (3 2 0) (3 2) (1 1) (1) (0))


; Problem 19

;; A list of all ways to partition TOTAL, where  each partition must
;; be at most MAX-VALUE and there are at most MAX-PIECES partitions.
(define (list-partitions total max-pieces max-value)
  ; *** YOUR CODE HERE ***
    (define (helper total pieces max sofar)
        (cond 
            ((= total 0) (list sofar))
            ((< total 0) nil)
            ((= max 0)   nil)
            ((= pieces 0)nil)
            (else 
                (append
                    (helper total pieces (- max 1) sofar) 
                    (helper (- total max) (- pieces 1) max (append sofar (list max)))
                )
            )
        )
    )
    (helper total max-pieces max-value nil)
)

; Problem 19 tests rely on correct Problem 18.
(sort-lists (list-partitions 5 2 4))
; expect ((4 1) (3 2))
(sort-lists (list-partitions 7 3 5))
; expect ((5 2) (5 1 1) (4 3) (4 2 1) (3 3 1) (3 2 2))


; Problem 20

;; The Tree abstract data type has an entry and a list of children.
(define (make-tree entry children)
  (cons entry children))
(define (entry tree)
  (car tree))
(define (children tree)
  (cdr tree))

;; An example tree:
;;                5
;;       +--------+--------+
;;       |        |        |
;;       6        7        2
;;    +--+--+     |     +--+--+
;;    |     |     |     |     |
;;    9     8     1     6     4
;;                      |
;;                      |
;;                      3
(define tree
  (make-tree 5 (list
                (make-tree 6 (list
                              (make-tree 9 nil)
                              (make-tree 8 nil)))
                (make-tree 7 (list
                              (make-tree 1 nil)))
                (make-tree 2 (list
                              (make-tree 6 (list
                                            (make-tree 3 nil)))
                              (make-tree 4 nil))))))

;; Takes a TREE of numbers and outputs a list of sums from following each
;; possible path from root to leaf.

(define (flatten lol)
  (if (or (equal? lol nil) (null? lol) ) 
    nil
    (merge (lambda (a b) #t) (car lol) (flatten (cdr lol)))
  )
)

(define (tree-sums tree)
  ; *** YOUR CODE HERE ***
  (if (equal? (children tree) nil) (cons (entry tree) nil)
      (map (lambda (x) (+ (entry tree) x)) (flatten (map tree-sums (children tree)))))
)

(tree-sums tree)
; expect (20 19 13 16 11)


; Problem 21 (optional)

; Draw the hax image using turtle graphics.
(define (hax d k)
  ; *** YOUR CODE HERE ***
  nil)
