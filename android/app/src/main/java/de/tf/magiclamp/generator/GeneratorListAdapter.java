package de.tf.magiclamp.generator;

import android.app.Activity;
import android.app.Application;
import android.app.FragmentManager;
import android.content.Context;
import android.support.v7.widget.CardView;
import android.support.v7.widget.RecyclerView;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageButton;
import android.widget.TextView;

import java.util.List;

import butterknife.Bind;
import butterknife.ButterKnife;
import de.tf.magiclamp.HomeFragment;
import de.tf.magiclamp.R;
import de.tf.magiclamp.model.GeneratorConfig;
import de.tf.magiclamp.model.LampConfig;
import retrofit.Callback;
import retrofit.RetrofitError;
import retrofit.client.Response;

/**
 * Created by tf on 9/2/15.
 */
public class GeneratorListAdapter extends RecyclerView.Adapter<GeneratorListAdapter.ViewHolder> {
    private List<GeneratorConfig> values;
    private Context context;
    String TAG = "GeneratorListAdapter";

    // Provide a reference to the views for each data item
    // Complex data items may need more than one view per item, and
    // you provide access to all the views for a data item in a view holder
    public static class ViewHolder extends RecyclerView.ViewHolder {
        // each data item is just a string in this case
        @Bind(R.id.name_text)
        public TextView mTextView;
        @Bind(R.id.playButton)
        public ImageButton mPlayButton;
        @Bind(R.id.card_view)
        public CardView mCardView;

        public ViewHolder(View v) {
            super(v);
            ButterKnife.bind(this, v);
        }
    }

    public GeneratorListAdapter(List<GeneratorConfig> values, Context context) {
        this.values = values;
        this.context = context;
    }

    @Override
    public ViewHolder onCreateViewHolder(ViewGroup viewGroup, int viewType) {
        View itemView = LayoutInflater.
                from(viewGroup.getContext()).
                inflate(R.layout.generator_row, viewGroup, false);

        return new ViewHolder(itemView);
    }

    @Override
    public void onBindViewHolder(ViewHolder holder, int position) {
        final GeneratorListAdapter adapter = this;
        GeneratorConfig c = values.get(position);
        if (c.getGeneratorIndex() == HomeFragment.lampConfig.getGeneratorIndex()) {
            holder.mCardView.setBackgroundColor(context.getResources().getColor(R.color.cardview_active));
        } else {
            holder.mCardView.setBackgroundColor(context.getResources().getColor(R.color.cardview_light_background));
        }
        holder.mTextView.setText(c.getName());
        holder.mPlayButton.setTag(c.getGeneratorIndex());
        holder.mPlayButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                final int generatorIndex = Integer.parseInt(v.getTag().toString());
                HomeFragment.lampConfig.setGeneratorIndex(generatorIndex);
                HomeFragment.service.setConfig(HomeFragment.lampConfig, new Callback<LampConfig>() {
                    @Override
                    public void success(LampConfig lampConfig, Response response) {
                        Log.d(TAG, "success setting generator to " + generatorIndex);
                    }

                    @Override
                    public void failure(RetrofitError error) {
                        Log.e(TAG, "error", error);
                    }
                });
                adapter.notifyDataSetChanged();
            }
        });
        holder.mTextView.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Activity activity = (Activity) v.getContext();
                FragmentManager fragmentManager = activity.getFragmentManager();
                fragmentManager.beginTransaction()
                        .replace(R.id.container, FloatingPointGeneratorConfigFragment.newInstance("", "")).addToBackStack("")
                        .commit();
            }
        });
    }

    @Override
    public int getItemCount() {
        return values.size();
    }
}
