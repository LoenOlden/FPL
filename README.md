This is far from a commercial and advanced models, just a basic implementation of an FPL Solver, mainly focused on expected stats.

Preseason expected minutes was working great but everything changes so quickly with news and injuries so expectedminutes.py file is pretty much useless for now.

My advice is not to run that file but accept updated_player_data.py file as a base and make the changes there as you wish. I manually update expected minutes looking at fplreview's minutes.

You can update your minutes at updated_player_data.py, also can change xG and xA stats based on last couple of games or market odds. I almost totally used 23/24 premier league data by FPL API.

After making changes as you wish at updated_player_data.py file, then you can run fplformula.py file.

If you want smoother experience with solver, i advice you to manually delete the players whose projections are lower than 0.4 or 0.5 raw expected points at sorted_player_data.py file.

But be careful, if one of your players have less than 0.4 or 0.5 raw expected points you shouldn't delete them because you need to use them at initial_players with solver.

After that you can run fixturesformula.py file to have fixture based projections and it will create final_player_data.py file, which is necessary to solve at main.py.

There can be constraint problems at solver, because if a player rises 0.2, you can only sell 0.1 more, i didn't adapt this into the model so you should be careful at managing budget and you can
manually set the players prices at updated_player_data.py file if there are problems because of that. Bench budget is not much important, you can set it to 16.0 if you want no effect at all.

But if you want strong bench, then you can increase it to 18.5-20.5. Your choice. However you should check if you have already that pre-gameweek. Otherwise constraints can't be matched.

For hit value i advice it to be around 3.0, it shouldn't be less than 2.0 and shouldn't be more than 4.0. Ideal should be between 2.5 and 3.5. If you want aggressive transfers and hits approach then
can set it to 2.5. If you want no hits in general then 3.5 seems reasonable.

Decay rate is used for covering the uncertainty of future gameweeks. If you want no effect at all and if you want all gameweeks equally weighted then you should set it to 1.0. But in general
we value more what is closer. If you want to have more direct and very short term gain approach then you should set it less, could be 0.85 for example and it is easier to solve with less values.
I personally like to use 0.97 (3% lower every week, if the number of gameweeks are 8, then 1. gameweeks value is 1.00, 8. gameweeks value is 0.97^7 = 0.807. So 20% fall for 8. gameweek which seems
ideal to me because information changes a lot. Decay rate generally should be 0.94-0.98. Also if you value future gameweeks more then you can set it more than 1 like 1.03, 1.04 etc. but it doesn't make much
sense at all.

With num_weeks parameter you just set how many weeks you want to solve. My advice is around 6 should be fine. More than 8 make the things harder for solver and solving less than 3 gameweeks doesn't make
sense at all, if you want to use free hit then you can set it to 1 and see the best. Also there is mainwildcard.py file, whatever gameweek you want to wildcard you can set that week and you can see afterwards,
the transfer plans.

New rolling up to 5 free transfers is hard to implement and tough for solver in general so i use max transfers per week and 2 looks fine in general. If you want no hit approach then you can set it to 1.
Important thing is if you set it more than 3, also with high number of weeks then solver will take minutes to find a solution which is not ideal.

You can set banned_players, players you don't want at all, and the players you want every gameweeks, you can set it with locked_players. You should set 15 initial_players for solver to work properly.
The problem is there are some players who share same name in the game, examples are Ward, Martinez, Wood, Johnson so if you have one of those players, you should get rid of others by commenting them out
at final_player_data.py or you can set new names for other players (adding their surnames or names for example).

Also i want to say this is not a guarantee for future success at FPL, just a basic helping tool and my personal hobby project for managing my team with an analytical approach.
That's pretty much it.
