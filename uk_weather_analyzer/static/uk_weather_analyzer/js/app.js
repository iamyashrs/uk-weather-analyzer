(function () {
    'use strict';

    var MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
    Chart.defaults.global.defaultFontColor = '#000';

    var app = angular.module('app', ['ngAnimate','angular-kudos','chart.js','ui.bootstrap','cgBusy']);

    app.config(function (ChartJsProvider) {
        // Configure all charts
        ChartJsProvider.setOptions({
          colors: ['#97BBCD', '#DCDCDC', '#F7464A', '#46BFBD', '#FDB45C', '#949FB1', '#4D5360']
        });
        // Configure all doughnut charts
        ChartJsProvider.setOptions('doughnut', {
          cutoutPercentage: 60
        });
        ChartJsProvider.setOptions('bubble', {
          tooltips: { enabled: false }
        });
    });

    app.controller('MainCtrl', function($scope, $http) {
        $scope.addCount = function(){
            $scope.cfdump = "";

            // function getCookie(name) {
            //     var cookieValue = null;
            //     if (document.cookie && document.cookie !== '') {
            //         var cookies = document.cookie.split(';');
            //         for (var i = 0; i < cookies.length; i++) {
            //             var cookie = jQuery.trim(cookies[i]);
            //             // Does this cookie string begin with the name we want?
            //             if (cookie.substring(0, name.length + 1) === (name + '=')) {
            //                 cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            //                 break;
            //             }
            //         }
            //     }
            //     return cookieValue;
            // }
            // var csrftoken = getCookie('csrftoken');
            //
            // $http.defaults.xsrfCookieName['csrftoken'] = csrftoken;
            // $http.defaults.headers.post['X-CSRFToken'] = csrftoken;
            //
            // function csrfSafeMethod(method) {
            //     // these HTTP methods do not require CSRF protection
            //     return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
            // }
            // $.ajaxSetup({
            //     beforeSend: function(xhr, settings) {
            //         if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            //             xhr.setRequestHeader("X-CSRFToken", csrftoken);
            //         }
            //     }
            // });

            var request = $http({
                method: "post",
                url: "/kudos",
                data: {
                    count: 1
                }
            });

            // Store the data-dump of the FORM scope.
            request.success(
                function( html ) {
                    $scope.cfdump = html;
                    $('#kudu_count').html(html.count);
                }
            );
        };
    });

    app.controller('LineCtrl', ['$scope','$http', function ($scope, $http) {
        $scope.show = true;

        function update_table() {
            $scope.myPromise = $http.get('/api/readings?region=' + $scope.region + '&mode=' + $scope.mode )
                   .then(function(res){

                        var years = [], ann = [], win = [], sum = [], aut = [], spr = [], max_value = 0, min_value = 0,
                            newest_year_month_data = [], newest_year_previous_year_data = [];

                        for (var i = 0; i < res.data.results.length; i++) {
                           years.push(res.data.results[i].Year);
                           ann.push(res.data.results[i].ANN);
                           win.push(res.data.results[i].WIN);
                           sum.push(res.data.results[i].SUM);
                           spr.push(res.data.results[i].SPR);
                           aut.push(res.data.results[i].AUT);
                           var tmp = Amin([res.data.results[i].ANN, res.data.results[i].WIN,
                           res.data.results[i].SUM, res.data.results[i].SPR, res.data.results[i].AUT]);
                           var tmp2 = Amax([res.data.results[i].ANN, res.data.results[i].WIN,
                           res.data.results[i].SUM, res.data.results[i].SPR, res.data.results[i].AUT]);
                           if (tmp < min_value){
                               min_value = tmp;
                           }
                           if (tmp2 > max_value){
                               max_value = tmp2;
                           }
                           if(res.data.results.length-1 == i){
                               $scope.newest_year = res.data.results[i].Year;
                               $scope.updated_at = res.data.results[i].updated_at;
                               newest_year_month_data.push(res.data.results[i].JAN, res.data.results[i].FEB,
                               res.data.results[i].MAR, res.data.results[i].APR, res.data.results[i].MAY,
                               res.data.results[i].JUN, res.data.results[i].JUL, res.data.results[i].AUG,
                               res.data.results[i].SEP, res.data.results[i].OCT, res.data.results[i].NOV,
                               res.data.results[i].DEC);
                           } else if ((res.data.results.length-2) == i){
                               newest_year_previous_year_data.push(res.data.results[i].JAN, res.data.results[i].FEB,
                               res.data.results[i].MAR, res.data.results[i].APR, res.data.results[i].MAY,
                               res.data.results[i].JUN, res.data.results[i].JUL, res.data.results[i].AUG,
                               res.data.results[i].SEP, res.data.results[i].OCT, res.data.results[i].NOV,
                               res.data.results[i].DEC);
                           }
                        }
                        // console.log(max_value);
                        // console.log(min_value);

                        $scope.type = 'line';
                        $scope.labels = years;
                        $scope.series = ['Annual', 'Winter', 'Summer', 'Spring', 'Autumn'];
                        $scope.data = [ann, win, sum, spr, aut];

                        $scope.onClick = function (points, evt) {
                          console.log(points, evt);
                        };
                        $scope.onHover = function (points) {
                          if (points.length > 0) {
                            console.log('Point', points[0].value);
                          } else {
                            console.log('No point');
                          }
                        };

                        if($scope.mode == 'Max Temp' || $scope.mode == 'Mean Temp' || $scope.mode == 'Min Temp'){
                            $scope.value_type = '°C';
                        } else if ($scope.mode == 'Sunshine'){
                            $scope.value_type = 'Total hours';
                        } else if ($scope.mode == 'Rainfall') {
                            $scope.value_type = 'Millimeters';
                        } else {
                            $scope.value_type = 'Value';
                        }

                        $scope.options = {
                            responsive: true,
                            legend: {
                                position: 'bottom',
                            },
                            scales: {
                                xAxes: [{
                                    display: true,
                                    scaleLabel: {
                                        display: true,
                                        labelString: 'Year'
                                    },
                                    gridLines : {
                                        display : false
                                    }
                                }],
                                yAxes: [{
                                    display: true,
                                    scaleLabel: {
                                        display: true,
                                        labelString: $scope.value_type
                                    },
                                    ticks: {
                                        suggestedMin: min_value+1,
                                        suggestedMax: max_value-1,
                                    },
                                    gridLines : {
                                        display : false
                                    }
                                }]
                            }
                        };

                    //    2016 chart starts here
                       $scope.newest_year_max_value = Amax(newest_year_month_data);
                       $scope.newest_year_min_value = Amin(without(newest_year_month_data, null));
                       $scope.newest_years_previous_year_max_value = Amax(newest_year_previous_year_data);
                       $scope.newest_years_previous_year_min_value = Amin(newest_year_previous_year_data);

                       $scope.bar_colors = ['#45b7cd', '#ff6384', '#ff8e72'];
                       $scope.bar_labels = MONTHS;
                        $scope.bar_data = [ newest_year_month_data, newest_year_previous_year_data];
                       $scope.bar_options = {
                                scaleShowVerticalLines: false,
                                scaleShowHorizontalLines: false,
                                responsive: true,
                                legend: {
                                    position: 'bottom'
                                },
                                title:{
                                    display:true,
                                    text:$scope.newest_year + ' vs ' + ($scope.newest_year-1)
                                },
                                scales: {
                                    xAxes: [{
                                        display: true,
                                        scaleLabel: {
                                            display: true,
                                            labelString: 'Month'
                                        },
                                        gridLines : {
                                            display : false
                                        }
                                    }],
                                    yAxes: [{
                                        display: true,
                                        scaleLabel: {
                                            display: true,
                                            labelString: $scope.value_type
                                        },
                                        gridLines : {
                                            display : false
                                        }
                                    }]
                                }
                       };

                        $scope.bar_datasetOverride = [
                          {
                            label: $scope.newest_year,
                            borderWidth: 1,
                            type: 'bar'
                          },
                          {
                            label: ($scope.newest_year-1),
                            borderWidth: 3,
                            hoverBackgroundColor: "rgba(255,99,132,0.4)",
                            hoverBorderColor: "rgba(255,99,132,1)",
                            type: 'line'
                          }
                        ];

                    //    Facts
                         $scope.new_prev_year_diff = Number((Amean(diff_arr(newest_year_previous_year_data.slice(0,
                             without(newest_year_month_data, null).length), without(newest_year_month_data, null)))).toFixed(1));

                       $scope.show = false;
                    });
        }

        $http.get('/api/modes')
               .then(function(res){
                    var modes_dict = res.data.results;

                    $scope.modes = [];
                    for(var i=0; i<modes_dict.length; i++){
                        $scope.modes.push(modes_dict[i].Name);
                    }

                    $scope.mode = modes_dict[0].Name;
                    $scope.activeMenu = $scope.mode;
                });

        $http.get('/api/regions')
               .then(function(res){
                    var regions_dict = res.data.results;

                    $scope.button = regions_dict[0].Name;
                    $scope.regions = [];
                    for(var i=0; i<regions_dict.length; i++){
                        $scope.regions.push(regions_dict[i].Name);
                    }

                    $scope.region = regions_dict[0].Name;
                });

        $scope.region_change = function(region){
            $scope.button = region;
            $scope.region = region;
            update_table();
        };

        $scope.mode_change = function(mode){
            $scope.mode = mode;
            $scope.activeMenu = mode;
            update_table();
        };

        if ($scope.region != null && $scope.mode != null){
            update_table();
        } else {
            $scope.region = "UK";
            $scope.mode = "Max Temp";
            update_table();
        }
    }]);

    function getRandomValue (data) {
        var l = data.length, previous = l ? data[l - 1] : 50;
        var y = previous + Math.random() * 10 - 5;
        return y < 0 ? 0 : y > 100 ? 100 : y;
    }

    function without(array, what){
        return array.filter(function(el){
            return el !== what;
        });
    }

    //avoid redefining prototypes - caused issues with diagrams not appearing in some browsers
    function Asum(array)
    //sums all the elements of an array
    {
      var tot = 0;
      for (var i=0;i<array.length;i++) {tot += +array[i];}
      return tot;
    }

    function Amean(array)
    //calculates mean of an array
    {
        return Asum(array)/array.length;
    }

    function Amax(array) {
    //finds the maximum value in an array
      return Math.max.apply(Math, array);
    }

    function Amin(array) {
    //finds the minimum value in an array
      return Math.min.apply(Math, array);
    }

    function diff_arr(a, b){
        //Assuming both arrays are of same length
          var tot = [];
          for (var i=0;i<a.length;i++) {tot.push(Math.abs(a[i]-b[i]));}
          return tot;
    }


    function Aabs(array)
    //returns an array with all elements changed to their absolute value
    {
        var vec = array;
        for (var i=0;i<array.length;i++) {vec[i] = Math.abs(vec[i]);}
        return vec;
    }

})();
